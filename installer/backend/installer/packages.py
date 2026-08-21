import os
import shutil


class PackageManager:
    def __init__(self, installer):
        self.installer = installer

    def configure_mirrors(self):
        self.installer.set_status(
            "configuring mirrors"
        )

        mirrorlist = (
            "/etc/pacman.d/mirrorlist"
        )

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
        self.installer.set_status(
            "preparing keyring"
        )

        keyring = (
            "/etc/pacman.d/gnupg"
        )

        if os.path.exists(keyring):
            shutil.rmtree(keyring)

        os.makedirs(
            keyring,
            mode=0o700,
            exist_ok=True
        )

        self.installer.run([
            "pacman-key",
            "--init"
        ])

        self.installer.run([
            "pacman-key",
            "--populate",
            "archlinux"
        ])

    def install_base(self):
        self.installer.set_status(
            "installing"
        )

        self.configure_mirrors()
        self.prepare_keyring()

        self.installer.run([
            "pacstrap",
            "-K",
            "/mnt",
            "base",
            "linux",
            "linux-firmware",
            "networkmanager",
            "sudo"
        ])