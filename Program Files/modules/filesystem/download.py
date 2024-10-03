import logging
import os
import urllib
import urllib.request
import time

from .verify import verify

from .exceptions import FileSystemError


def download(url: str, destination: str, attempts: int = 3) -> None:
    logging.info("Attempt to download file from \""+url+"\"")
    try:
        verify(os.path.dirname(destination), create_missing_directories=True)
        urllib.request.urlretrieve(url, destination)
    
    except Exception as e:
        logging.warning("File download failed!")
        logging.error(type(e).__name__+": "+str(e))
    

        if attempts > 0:
            time.sleep(2)
            logging.info("Retrying . . .")
            return download(url=url, destination=destination, attempts=attempts-1)
        
        else:
            logging.error("Too many attempts!")
            raise type(e)(str(e))