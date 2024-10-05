import logging
import os

from modules.filesystem.files import File
from modules.filesystem.directories import Directory
from modules.filesystem.verify import verify

from .exceptions import CoreFileNotFoundError


def check_required_files() -> None:
    try:
        required_files: list[str] = File.all()
        root: str = Directory.root()

        missing_files: list[str] = []
        for file in required_files:
            try:
                verify(file)
            except Exception as e:
                logging.error(f'Core file not found: {file.removeprefix(root)}')
                missing_files.append(os.path.basename(file))
        
        if missing_files != []:
            raise CoreFileNotFoundError(f'The following core file(s) are missing: {', '.join(missing_files)}')
    
    except Exception as e:
        logging.error(type(e).__name__+": "+str(e))
        raise type(e)(str(e))