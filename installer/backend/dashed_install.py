import subprocess

from installer.disks import DiskManager
from installer.filesystem import FilesystemManager
from installer.packages import PackageManager
from installer.system import SystemManager
from installer.users import UserManager
from installer.network import NetworkManager
from installer.bootloader import BootloaderManager


class DashedInstall:
    def __init__(self):
        self.status = "ready"

        self.disks = DiskManager(self)
        self.filesystem = FilesystemManager(self)
        self.packages = PackageManager(self)
        self.system = SystemManager(self)
        self.users = UserManager(self)
        self.network = NetworkManager(self)
        self.bootloader = BootloaderManager(self)

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return {
            "status": self.status
        }

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

    def run_input(self, command, input_text):
        print(
            "RUNNING:",
            " ".join(command),
            flush=True
        )

        result = subprocess.run(
            command,
            input=input_text,
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

    def get_disks(self):
        return self.disks.get_disks()

    def install(self, config):
        disk = config.get("disk")

        if not disk:
            raise ValueError(
                "No installation disk selected."
            )

        self.disks.validate_disk(
            disk
        )

        self.disks.partition(
            disk
        )

        self.filesystem.format(
            disk
        )

        self.filesystem.mount(
            disk
        )

        self.packages.install_base()

        self.filesystem.generate_fstab()

        self.system.configure(
            config
        )

        self.users.create(
            config["username"],
            config["password"]
        )

        self.network.configure()
        
        self.bootloader.install()

        self.status = (
            "Installed"
        )

        return {
            "status": self.status,
            "disk": disk,
            "hostname": config.get(
                "hostname"
            ),
            "username": config.get(
                "username"
            )
        }