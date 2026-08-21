class SystemManager:
    def __init__(self, installer):
        self.installer = installer

    def configure(self, config):
        self.installer.set_status(
            "configuring system"
        )

        self.set_hostname(
            config.get(
                "hostname",
                "dashed"
            )
        )

        self.set_locale(
            config.get(
                "language",
                "en"
            )
        )

        self.set_keyboard(
            config.get(
                "keyboard",
                "us"
            )
        )

    def set_hostname(self, hostname):
        hostname = hostname.strip()

        if not hostname:
            raise ValueError(
                "Hostname cannot be empty."
            )

        if len(hostname) > 63:
            raise ValueError(
                "Hostname cannot be longer than 63 characters."
            )

        with open(
            "/mnt/etc/hostname",
            "w"
        ) as f:
            f.write(
                hostname + "\n"
            )

    def set_locale(self, language):
        locale_map = {
            "en": "en_US.UTF-8",
            "nl": "nl_NL.UTF-8",
            "fr": "fr_FR.UTF-8",
            "de": "de_DE.UTF-8",
            "es": "es_ES.UTF-8"
        }

        locale = locale_map.get(
            language,
            "en_US.UTF-8"
        )

        locale_gen = (
            "/mnt/etc/locale.gen"
        )

        with open(
            locale_gen,
            "r"
        ) as f:
            lines = f.readlines()

        new_lines = []

        for line in lines:
            stripped = (
                line.strip()
                .lstrip("#")
                .strip()
            )

            if stripped == (
                f"{locale} UTF-8"
            ):
                new_lines.append(
                    f"{locale} UTF-8\n"
                )
            else:
                new_lines.append(
                    line
                )

        with open(
            locale_gen,
            "w"
        ) as f:
            f.writelines(
                new_lines
            )

        self.installer.run([
            "arch-chroot",
            "/mnt",
            "locale-gen"
        ])

        with open(
            "/mnt/etc/locale.conf",
            "w"
        ) as f:
            f.write(
                f"LANG={locale}\n"
            )

    def set_keyboard(self, keyboard):
        keyboard_map = {
            "us": "us",
            "uk": "uk",
            "nl": "nl",
            "de": "de",
            "fr": "fr"
        }

        layout = keyboard_map.get(
            keyboard,
            "us"
        )

        with open(
            "/mnt/etc/vconsole.conf",
            "w"
        ) as f:
            f.write(
                f"KEYMAP={layout}\n"
            )