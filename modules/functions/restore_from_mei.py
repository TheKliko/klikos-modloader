import os
import shutil
import sys

from modules.logger import logger
from modules.filesystem import Directory, logged_path


IS_FROZEN = getattr(sys, "frozen", False)


class FileRestoreError(Exception):
    pass


def restore_from_mei(file: str) -> None:
    if not IS_FROZEN:
        error_text = f"Failed to restore file: {logged_path.get(file)}, reason: IS_FROZEN == False"
        logger.error(error_text)
        raise FileRestoreError(error_text)
    
    MEIPASS: str = Directory._MEI()
    root: str = Directory.root()
    relative_path: str = os.path.relpath(file, root)

    if not os.path.isfile(os.path.join(MEIPASS, relative_path)):
        error_text = f"Failed to restore file: {logged_path.get(file)}, reason: File does not exist"
        logger.error(error_text)
        raise FileRestoreError(error_text)

    try:
        os.makedirs(os.path.dirname(file), exist_ok=True)
        shutil.copy(os.path.join(MEIPASS, relative_path), os.path.join(root, relative_path))
        logger.info(f"File restored from _MEI: {logged_path.get(file)}")

    except shutil.SameFileError:
        pass

    except Exception as e:
        logger.error(f"Failed to restore file: {logged_path.get(file)}, reason: {type(e).__name__}: {e}")
        raise