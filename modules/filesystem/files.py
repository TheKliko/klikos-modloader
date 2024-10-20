import os

from .directories import Directory


class FilePath:
    @staticmethod
    def settings() -> str:
        return os.path.join(Directory.config(), "settings.json")

    @staticmethod
    def integrations() -> str:
        return os.path.join(Directory.config(), "integrations.json")

    @staticmethod
    def mods() -> str:
        return os.path.join(Directory.config(), "mods.json")

    @staticmethod
    def fastflags() -> str:
        return os.path.join(Directory.config(), "fastflags.json")

    @staticmethod
    def launch_integrations() -> str:
        return os.path.join(Directory.config(), "launch_integrations.json")
    
    @staticmethod
    def core_files() -> list[str]:
        return [
            FilePath.settings(),
            FilePath.integrations()
        ]