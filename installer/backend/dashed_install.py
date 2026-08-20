import json
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
        disks = self.get_disks()

        for disk in disks:
            if disk["device"] == device:
                return disk

        raise ValueError("Disk not found")

    def partition_disk(self, device):
        disk = self.get_disk(device)

        self.status = "partitioning"

        subprocess.run(
            ["umount", f"{device}1"],
            check=False
        )

        subprocess.run(
            ["umount", f"{device}2"],
            check=False
        )

        subprocess.run(
            [
                "sgdisk",
                "--zap-all",
                device
            ],
            check=True
        )

        subprocess.run(
            [
                "sgdisk",
                "-n", "1:0:+1G",
                "-t", "1:ef00",
                "-c", "1:EFI",
                device
            ],
            check=True
        )

        subprocess.run(
            [
                "sgdisk",
                "-n", "2:0:0",
                "-t", "2:8300",
                "-c", "2:Dashed",
                device
            ],
            check=True
        )

        subprocess.run(
            ["partprobe", device],
            check=False
        )

        self.status = "partitioned"

        return {
            "status": self.status,
            "disk": device
        }

    def install(self, config):
        disk = config.get("disk")

        if not disk:
            raise ValueError(
                "No installation disk selected"
            )

        return self.partition_disk(disk)