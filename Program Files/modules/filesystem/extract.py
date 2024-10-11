import logging
import os
import zipfile

from .verify import verify
from .exceptions import FileSystemError


def extract(source: str, destination: str) -> None:
    logging.info("Extracting file "+str(os.path.basename(source))+" . . .")
    try:
        verify(source)
        verify(destination, create_missing_directories=True)
        
        if source.endswith(".zip"):
            with zipfile.ZipFile(source, "r") as zip:
                zip.extractall(destination)
                zip.close()
        
        # elif source.endswith(".7z"):
        #     with py7zr.SevenZipFile(source, mode='r') as archive:
        #         archive.extractall(path=destination)
        
        # elif source.endswith(".rar"):
        #     with rarfile.RarFile(source) as archive:
        #         archive.extractall(path=destination)
            
        else:
            raise FileSystemError("Failed to extract \""+str(os.path.basename(source))+"\", unsupported file format.")
    
    except Exception as e:
        logging.warning("File extraction failed!")
        logging.error(type(e).__name__+": "+str(e))
        raise type(e)(str(e))