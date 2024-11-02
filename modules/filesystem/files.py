import os

from .directories import Directory


class FilePath:
    @staticmethod
    def settings() -> str:
        return os.path.join(Directory.config(), "settings.json")
    
    @staticmethod
    def skip_platform_check() -> str:
        return os.path.join(Directory.config(), "SKIP_PLATFORM_CHECK")
    
    @staticmethod
    def core_files() -> list[str]:
        return [
            FilePath.settings()
        ]