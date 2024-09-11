import os

from .directories import Directory


class FilePath:
    INTEGRATIONS: str = None
    SETTINGS: str = None
    MODS: str = None
    FASTFLAGS: str = None

    _initialized: bool = False

    @classmethod
    def initialize(cls) -> None:
        if cls._initialized == False:
            if Directory._initialized == False:
                Directory.initialize()
            cls.INTEGRATIONS: str = os.path.join(Directory.PROGRAM_FILES, 'config', 'integrations.json')
            cls.SETTINGS: str = os.path.join(Directory.PROGRAM_FILES, 'config', 'settings.json')
            cls.MODS: str = os.path.join(Directory.PROGRAM_FILES, 'config', 'mods.json')
            cls.FASTFLAGS: str = os.path.join(Directory.PROGRAM_FILES, 'config', 'fastflags.json')
            cls._initialized = True
