import logging
import os

from .exceptions import FileSystemError
from . import logged_path


def verify(path: str, create_missing_directories: bool = False, create_missing_file: bool = False) -> None:
    try:
        if not os.path.exists(path):
            if create_missing_directories == False and create_missing_file == False:
                raise FileSystemError(f"Path does not exist: {logged_path.get(path)}")
            
            os.makedirs(path, exist_ok=True)
            
            if create_missing_file == True:
                with open(path, "w") as file:
                    file.close()

    except Exception as e:
        logging.error(type(e).__name__+": "+str(e))
        raise type(e)(str(e))