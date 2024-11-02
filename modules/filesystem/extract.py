import os
import zipfile

# import py7zr
# import rarfile

from modules.logger import logger

from .verify import verify
from .exceptions import FileSystemError


def extract(source: str, destination: str) -> None:
    logger.info(f"Extracting file \"{os.path.basename(source)}\"...")
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
            logger.error(f"Failed to extract \"{os.path.basename(source)}\", reason: unsupported file format!")
            raise FileSystemError(f"Failed to extract \"{os.path.basename(source)}\", reason: unsupported file format!")
    
    except FileSystemError:
        raise
    
    except Exception as e:
        logger.error(f"Failed to extract \"{os.path.basename(source)}\", reason: {type(e).__name__}! {e}")
        raise