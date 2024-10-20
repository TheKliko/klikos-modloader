import os
import shutil

from modules.logger import logger

from . import logged_path


def remove(path: str) -> None:

    log_path: str = logged_path.get(path)
    logger.info(f"Removing {log_path}...")

    try:
        if os.path.isdir(path):
            shutil.rmtree(path=path)
        elif os.path.isfile(path):
            os.remove(path=path)

    except Exception as e:
        logger.error(f"Failed to remove {log_path}")
        raise type(e)(str(e))