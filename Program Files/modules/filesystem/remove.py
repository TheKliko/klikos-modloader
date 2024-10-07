import logging
import os
import shutil


def remove(path: str) -> None:
    try:
        if os.path.isdir(path):
            shutil.rmtree(path=path)
        elif os.path.isfile(path):
            os.remove(path=path)

    except Exception as e:
        logging.error(type(e).__name__+": "+str(e))
        raise type(e)(str(e))