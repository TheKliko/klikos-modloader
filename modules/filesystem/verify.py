import logging
import os

from .exceptions import FileSystemError
from . import logged_path


def verify(path: str, create_missing_directories: bool = False, create_missing_file: bool = False) -> None:
    try:
        if not os.path.exists(path):
            if create_missing_directories is False and create_missing_file is False:
                raise FileSystemError(f"Path does not exist: {logged_path.get(path)}")
            
            if create_missing_file is True:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w") as file:
                    file.close()

            else:
                os.makedirs(path)

    except Exception as e:
        logging.error(type(e).__name__+": "+str(e))
        raise type(e)(str(e))