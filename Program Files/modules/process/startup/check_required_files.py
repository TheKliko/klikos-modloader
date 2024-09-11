import logging
import os

from modules.interface import Print, Color
from modules.other.paths import FilePath, Directory
from modules.utils import filesystem

from .exceptions import CoreFileMissingError


def check_required_files() -> None:
    logging.info('Checking required files . . .')
    Print('Checking required files . . .', color=Color.INITALIZE)

    required_files: list[str] = [
        getattr(FilePath, attr_name)
        for attr_name in FilePath.__dict__
        if not attr_name.startswith("__") and not callable(getattr(FilePath, attr_name))
    ]
    root: str = Directory.ROOT

    missing_files: list[str] = []
    for file in required_files:
        try:
            filesystem.verify(file)
        except Exception as e:
            logging.error(f'Core file not found: {file.removeprefix(root)}')
            missing_files.append(os.path.basename(file))
    
    if missing_files != []:
        raise CoreFileMissingError(f'The following core file(s) are missing: {', '.join(missing_files)}')