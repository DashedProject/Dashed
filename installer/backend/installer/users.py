import os


class UserManager:
    def __init__(self, installer):
        self.installer = installer

    def create(self, username, password):
        self.installer.set_status(
            "creating user"
        )

        username = username.strip()

        if not username:
            raise ValueError(
                "Username cannot be empty."
            )

        if " " in username:
            raise ValueError(
                "Username cannot contain spaces."
            )

        self.installer.run([
            "arch-chroot",
            "/mnt",
            "useradd",
            "-m",
            "-G",
            "wheel",
            "-s",
            "/bin/bash",
            username
        ])

        self.set_password(
            username,
            password
        )

        self.configure_sudo()

    def set_password(self, username, password):
        result = self.installer.run_input(
            [
                "arch-chroot",
                "/mnt",
                "chpasswd"
            ],
            f"{username}:{password}\n"
        )

        return result

    def configure_sudo(self):
        sudoers = (
            "/mnt/etc/sudoers.d/wheel"
        )

        with open(
            sudoers,
            "w"
        ) as f:
            f.write(
                "%wheel ALL=(ALL:ALL) ALL\n"
            )

        os.chmod(
            sudoers,
            0o440
        )