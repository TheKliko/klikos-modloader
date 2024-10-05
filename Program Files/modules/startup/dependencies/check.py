import json
import logging
import os

from .is_installed import is_installed
from .install import install


def check() -> None:
    try:
        with open(os.path.join(os.path.dirname(__file__), 'libraries.json'), 'r') as file:
            data: dict = json.load(file)
            file.close()

        for library in data:
            if is_installed(library) == False:
                install(library)
            else:
                continue


    except Exception as e:
        logging.error(type(e).__name__+": "+str(e))
        raise type(e)(str(e))