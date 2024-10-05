import os


class Directory:
    @staticmethod
    def root() -> str:
        return os.path.dirname(Directory.program_files())

    @staticmethod
    def logs() -> str:
        return os.path.join(Directory.root(), "Logs")

    @staticmethod
    def mods() -> str:
        return os.path.join(Directory.root(), "Mods")

    @staticmethod
    def versions() -> str:
        return os.path.join(Directory.root(), "Versions")

    @staticmethod
    def program_files() -> str:
        return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    @staticmethod
    def config() -> str:
        return os.path.join(Directory.program_files(), "config")