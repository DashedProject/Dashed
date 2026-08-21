import json
import subprocess


class DiskManager:
    def __init__(self, installer):
        self.installer = installer

    def get_disks(self):
        result = self.installer.run([
            "lsblk",
            "-J",
            "-d",
            "-o",
            "NAME,SIZE,MODEL,TYPE"
        ])

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

    def validate_disk(self, device):
        for disk in self.get_disks():
            if disk["device"] == device:
                return disk

        raise ValueError(
            f"Disk not found: {device}"
        )

    def partition(self, device):
        self.installer.set_status(
            "partitioning"
        )

        self.installer.run([
            "sgdisk",
            "--zap-all",
            device
        ])

        self.installer.run([
            "sgdisk",
            "-n", "1:0:+1G",
            "-t", "1:ef00",
            "-c", "1:EFI",
            device
        ])

        self.installer.run([
            "sgdisk",
            "-n", "2:0:0",
            "-t", "2:8300",
            "-c", "2:Dashed",
            device
        ])

        self.installer.run([
            "blockdev",
            "--rereadpt",
            device
        ])

        self.installer.run([
            "udevadm",
            "settle"
        ])

    def get_partitions(self, device):
        result = self.installer.run([
            "lsblk",
            "-J",
            "-o",
            "NAME,PATH,TYPE,PARTN"
        ])

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
            if partition.get(
                "path",
                ""
            ).startswith(device)
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