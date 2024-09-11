import logging
import os
import zipfile

from .verify import verify
from .exceptions import FileSystemError


def extract(source: str, destination: str) -> None:
    logging.info(f'Extracting file "{os.path.basename(source)}" . . .')
    try:
        verify(source)
        verify(destination, create_missing_directories=True)
        
        with zipfile.ZipFile(source, 'r') as zip:
            zip.extractall(destination)
            zip.close()

    except Exception as e:
        logging.error(f'[{type(e).__name__}] {str(e)}')
        raise FileSystemError(f'[{type(e).__name__}] {str(e)}')