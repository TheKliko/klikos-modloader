import os

from modules.utils import variables


class Directory:
    ROOT: str = None
    LOGS: str = None
    PROGRAM_FILES: str = None
    MODS: str = None
    VERSIONS: str = None
    CONFIG: str = None
    
    ROBLOX_LOCALAPPDATA: str = None

    _initialized: bool = False

    @classmethod
    def initialize(cls) -> None:
        if cls._initialized == False:
            cls.ROOT: str = variables.get('root')
            cls.LOGS: str = os.path.join(cls.ROOT, 'Logs')
            cls.PROGRAM_FILES: str = os.path.join(cls.ROOT, 'Program Files')
            cls.MODS: str = os.path.join(cls.ROOT, 'Mods')
            cls.VERSIONS: str = os.path.join(cls.ROOT, 'Versions')
            cls.CONFIG: str = os.path.join(cls.PROGRAM_FILES, 'config')
            cls.ROBLOX_LOCALAPPDATA: str = os.path.join(os.getenv('LOCALAPPDATA'), 'Roblox')
            cls._initialized = True