import logging
import os
import shutil

from .exceptions import FileSystemError
from . import verify


def remove(source: str) -> None:
    logging.info(f'Attempt to remove "{source}"')

    try:
        if os.path.isdir(source):
            shutil.rmtree(source)

        elif os.path.isfile(source):
            os.remove(source)

    except Exception as e:
        logging.warning(f'[FileSystemError] [{type(e).__name__}] {str(e)}')