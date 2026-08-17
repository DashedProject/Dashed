class DashedInstall:
    def __init__(self):
        self.status = "ready"

    def get_status(self):
        return {
            "status": self.status
        }