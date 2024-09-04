import logging
import os
import urllib
import urllib.request

from .verify import verify

from .exceptions import FileSystemError


def download(url: str, destination: str) -> None:
    logging.info(f'Attempt to download file from "{url}"')
    try:
        verify(os.path.dirname(destination), create_missing_directories=True)
        urllib.request.urlretrieve(url, destination)

    except Exception as e:
        logging.error(f'[{type(e).__name__}] {str(e)}')
        raise FileSystemError(f'[{type(e).__name__}] {str(e)}')