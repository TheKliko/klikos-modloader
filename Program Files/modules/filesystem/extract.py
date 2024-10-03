import logging
import os
import zipfile

from .verify import verify


def extract(source: str, destination: str) -> None:
    logging.info("Extracting file "+str(os.path.basename(source))+" . . .")
    try:
        verify(source)
        verify(destination, create_missing_directories=True)
        
        with zipfile.ZipFile(source, "r") as zip:
            zip.extractall(destination)
            zip.close()
    
    except Exception as e:
        logging.warning("File extraction failed!")
        logging.error(type(e).__name__+": "+str(e))
        raise type(e)(str(e))