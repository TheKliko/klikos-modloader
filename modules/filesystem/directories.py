import os
import sys


IS_FROZEN = getattr(sys, "frozen", False)


class Directory:
    @staticmethod
    def root() -> str:
        if IS_FROZEN:
            root = os.path.dirname(sys.executable)
        else:
            root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return root

    # @staticmethod
    # def logs() -> str:
    #     return os.path.join(Directory.root(), "Logs")

    @staticmethod
    def downloaded_mods() -> str:
        return os.path.join(Directory.root(), "Downloaded Mods")

    @staticmethod
    def bloxstrap_mods() -> str:
        return os.path.join(os.getenv("LOCALAPPDATA"), "Bloxstrap", "Modifications")

    @staticmethod
    def updated_mods() -> str:
        return os.path.join(Directory.root(), "Updated Mods")

    @staticmethod
    def config() -> str:
        return os.path.join(Directory.root(), "config")

    @staticmethod
    def _MEI() -> str:
        return sys._MEIPASS