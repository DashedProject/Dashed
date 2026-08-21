import os
import subprocess


class FilesystemManager:
    def __init__(self, installer):
        self.installer = installer

    def format(self, device):
        self.installer.set_status(
            "formatting"
        )

        efi_partition, root_partition = (
            self.installer.disks.get_partitions(
                device
            )
        )

        self.installer.run([
            "mkfs.fat",
            "-F", "32",
            "-n", "EFI",
            efi_partition
        ])

        self.installer.run([
            "mkfs.ext4",
            "-F",
            "-L", "Dashed",
            root_partition
        ])

        self.installer.run([
            "udevadm",
            "settle"
        ])

    def mount(self, device):
        self.installer.set_status(
            "mounting"
        )

        efi_partition, root_partition = (
            self.installer.disks.get_partitions(
                device
            )
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

        self.installer.run([
            "mount",
            root_partition,
            "/mnt"
        ])

        os.makedirs(
            "/mnt/boot",
            exist_ok=True
        )

        self.installer.run([
            "mount",
            efi_partition,
            "/mnt/boot"
        ])

    def generate_fstab(self):
        self.installer.set_status(
            "configuring fstab"
        )

        result = self.installer.run([
            "genfstab",
            "-U",
            "/mnt"
        ])

        with open(
            "/mnt/etc/fstab",
            "w"
        ) as f:
            f.write(
                result.stdout
            )