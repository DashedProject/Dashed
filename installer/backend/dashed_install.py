import json
import os
import shutil
import subprocess


class DashedInstall:
    def __init__(self):
        self.status = "ready"

    def get_status(self):
        return {
            "status": self.status
        }

    def get_disks(self):
        result = subprocess.run(
            [
                "lsblk",
                "-J",
                "-d",
                "-o",
                "NAME,SIZE,MODEL,TYPE"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        data = json.loads(result.stdout)

        disks = []

        for device in data["blockdevices"]:
            if device["type"] != "disk":
                continue

            disks.append({
                "device": f"/dev/{device['name']}",
                "size": device["size"],
                "model": device["model"] or "Unknown"
            })

        return disks

    def get_disk(self, device):
        for disk in self.get_disks():
            if disk["device"] == device:
                return disk

        raise ValueError("Disk not found")

    def run(self, command):
        print(
            "RUNNING:",
            " ".join(command),
            flush=True
        )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.stdout:
            print(
                result.stdout,
                flush=True
            )

        if result.stderr:
            print(
                result.stderr,
                flush=True
            )

        if result.returncode != 0:
            raise RuntimeError(
                f"Command failed with exit code "
                f"{result.returncode}: "
                f"{' '.join(command)}"
            )

        return result

    def partition_disk(self, device):
        self.status = "partitioning"

        self.run([
            "sgdisk",
            "--zap-all",
            device
        ])

        self.run([
            "sgdisk",
            "-n", "1:0:+1G",
            "-t", "1:ef00",
            "-c", "1:EFI",
            device
        ])

        self.run([
            "sgdisk",
            "-n", "2:0:0",
            "-t", "2:8300",
            "-c", "2:Dashed",
            device
        ])

        self.run([
            "blockdev",
            "--rereadpt",
            device
        ])

        self.run([
            "udevadm",
            "settle"
        ])

    def get_partitions(self, device):
        result = subprocess.run(
            [
                "lsblk",
                "-J",
                "-o",
                "NAME,PATH,TYPE,PARTN"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        data = json.loads(result.stdout)

        partitions = []

        def walk(devices):
            for entry in devices:
                if entry.get("type") == "part":
                    partitions.append(entry)

                if entry.get("children"):
                    walk(entry["children"])

        walk(data["blockdevices"])

        disk_partitions = [
            partition
            for partition in partitions
            if partition.get("path", "").startswith(device)
        ]

        disk_partitions.sort(
            key=lambda partition: int(
                partition["partn"]
            )
        )

        if len(disk_partitions) < 2:
            raise RuntimeError(
                f"Could not find partitions for {device}"
            )

        return (
            disk_partitions[0]["path"],
            disk_partitions[1]["path"]
        )

    def format_disk(self, device):
        self.status = "formatting"

        efi_partition, root_partition = (
            self.get_partitions(device)
        )

        self.run([
            "mkfs.fat",
            "-F", "32",
            "-n", "EFI",
            efi_partition
        ])

        self.run([
            "mkfs.ext4",
            "-F",
            "-L", "Dashed",
            root_partition
        ])

        self.run([
            "udevadm",
            "settle"
        ])

    def mount_disk(self, device):
        self.status = "mounting"

        efi_partition, root_partition = (
            self.get_partitions(device)
        )

        subprocess.run(
            [
                "umount",
                "-R",
                "/mnt"
            ],
            check=False
        )

        os.makedirs(
            "/mnt",
            exist_ok=True
        )

        self.run([
            "mount",
            root_partition,
            "/mnt"
        ])

        os.makedirs(
            "/mnt/boot",
            exist_ok=True
        )

        self.run([
            "mount",
            efi_partition,
            "/mnt/boot"
        ])

    def configure_mirrors(self):
        self.status = "configuring mirrors"

        mirrorlist = "/etc/pacman.d/mirrorlist"

        os.makedirs(
            "/etc/pacman.d",
            exist_ok=True
        )

        with open(
            mirrorlist,
            "w"
        ) as f:
            f.write(
                "Server = https://geo.mirror.pkgbuild.com/$repo/os/$arch\n"
            )

    def prepare_keyring(self):
        self.status = "preparing keyring"

        keyring = "/etc/pacman.d/gnupg"

        if os.path.exists(keyring):
            shutil.rmtree(keyring)

        os.makedirs(
            keyring,
            mode=0o700,
            exist_ok=True
        )

        self.run([
            "pacman-key",
            "--init"
        ])

        self.run([
            "pacman-key",
            "--populate",
            "archlinux"
        ])

    def install_base(self):
        self.status = "installing"

        self.configure_mirrors()

        self.prepare_keyring()

        self.run([
            "pacstrap",
            "-K",
            "/mnt",
            "base",
            "linux",
            "linux-firmware",
            "networkmanager",
            "sudo"
        ])

    def generate_fstab(self):
        self.status = "configuring"

        result = subprocess.run(
            [
                "genfstab",
                "-U",
                "/mnt"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        with open(
            "/mnt/etc/fstab",
            "w"
        ) as f:
            f.write(result.stdout)

    def install(self, config):
        disk = config.get("disk")

        if not disk:
            raise ValueError(
                "No installation disk selected."
            )

        self.get_disk(disk)

        self.partition_disk(disk)
        self.format_disk(disk)
        self.mount_disk(disk)
        self.install_base()
        self.generate_fstab()

        self.status = "installed"

        return {
            "status": "installed",
            "disk": disk
        }