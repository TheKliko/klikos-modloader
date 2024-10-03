import os

from .directories import Directory


class File:
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
    def all() -> list[str]:
        return [
            File.settings(),
            File.integrations(),
            File.mods(),
            File.fastflags()
        ]