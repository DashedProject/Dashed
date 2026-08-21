class NetworkManager:
    def __init__(self, installer):
        self.installer = installer

    def configure(self):
        self.installer.set_status(
            "configuring networking"
        )

        self.installer.run([
            "arch-chroot",
            "/mnt",
            "systemctl",
            "enable",
            "NetworkManager"
        ])