import logging
import os
import shutil

from .exceptions import FileSystemError
from . import verify


def copy(source: str, destination: str) -> None:
    verify(source)
    verify(destination, create_missing_directories=True)

    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)
            return
        
        destination: str = os.path.join(destination, os.path.basename(source))
        shutil.copyfile(source, destination)

    except Exception as e:
        logging.error(f'[{type(e).__name__}] {str(e)}')
        raise FileSystemError(f'[{type(e).__name__}] {str(e)}')