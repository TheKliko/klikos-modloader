import os
import zipfile

from modules.logger import logger

from .verify import verify
from .exceptions import FileSystemError
from . import logged_path


def compress(source: str, destination: str) -> None:
    logger.info(f"Compressing \"{os.path.basename(source)}\" to \"{os.path.basename(destination)}\"...")
    pass

    try:
        verify(source)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        if os.path.isfile(source) and (source.endswith(".zip") or source.endswith(".7z") or source.endswith(".rar")):
            logger.error("File is already compressed!")
            raise FileSystemError(f"Cannot compress already compressed file: \"{os.path.basename(source)}\"")

        with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as zip:
            if os.path.isfile(source):
                zip.write(source, os.path.basename(source))

            else:  # os.path.isdir(source)
                for dirpath, dirnames, filenames in os.walk(source):
                    for file in filenames:
                        file_path = os.path.join(dirpath, file)
                        arcname = os.path.relpath(file_path, start=source)
                        zip.write(file_path, arcname)
    
    except FileSystemError:
        raise
    
    except Exception as e:
        logger.error(f"Failed to extract \"{os.path.basename(source)}\", reason: {type(e).__name__}! {e}")
        raise