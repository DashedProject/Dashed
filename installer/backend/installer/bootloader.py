import os


class BootloaderManager:
    def __init__(self, installer):
        self.installer = installer

    def install(self):
        self.installer.set_status(
            "installing bootloader"
        )

        self.installer.run([
            "arch-chroot",
            "/mnt",
            "bootctl",
            "--path=/boot",
            "install"
        ])

        self.create_loader_config()
        self.create_boot_entry()

    def create_loader_config(self):
        loader_directory = (
            "/mnt/boot/loader"
        )

        os.makedirs(
            loader_directory,
            exist_ok=True
        )

        with open(
            f"{loader_directory}/loader.conf",
            "w"
        ) as f:
            f.write(
                "default dashed.conf\n"
                "timeout 5\n"
                "console-mode max\n"
                "editor no\n"
            )

    def create_boot_entry(self):
        entries_directory = (
            "/mnt/boot/loader/entries"
        )

        os.makedirs(
            entries_directory,
            exist_ok=True
        )

        entry = (
            f"{entries_directory}/dashed.conf"
        )

        with open(
            entry,
            "w"
        ) as f:
            f.write(
                "title Dashed\n"
                "linux /vmlinuz-linux\n"
                "initrd /initramfs-linux.img\n"
                "options root=LABEL=Dashed rw\n"
            )