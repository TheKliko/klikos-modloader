import os
import platform
import sys

from modules.interface import Color
from modules.functions import registry_keys

from . import logger
from .exceptions import PlatformError
from .check_required_files import check_required_files
from . import dependencies


def run() -> None:
    try:
        print(Color.INITIALIZE+"Starting logger . . .")
        logger.start()

        import logging
        logging.debug("Python version: "+str(sys.version_info.major)+"."+str(sys.version_info.minor)+"."+str(sys.version_info.micro)+"-"+str(sys.version_info.releaselevel))
        logging.debug("sys.argv = "+str(sys.argv))

        logging.info("Checking platform . . .")
        print(Color.INITIALIZE+"Checking platform . . .")
        system = platform.system()
        if system != "Windows":
            raise PlatformError("Unsupported OS \""+system+"\" detected. Currently, only Windows platforms are supported.")

        logging.info("Checking core files . . .")
        print(Color.INITIALIZE+"Checking core files . . .")
        check_required_files()
        from modules.filesystem import Directory
        os.makedirs(Directory.mods(), exist_ok=True)

        logging.info("Checking dependencies . . .")
        print(Color.INITIALIZE+"Checking dependencies . . .")
        dependencies.check()

        from . import update
        logging.info("Checking for updates . . .")
        print(Color.INITIALIZE+"Checking for updates . . .")
        update.check()

        logging.info("Setting registry keys . . .")
        print(Color.INITIALIZE+"Setting registry keys . . ."+Color.RESET)
        registry_keys.set()

        logging.info("Clearing old logs . . .")
        print(Color.INITIALIZE+"Clearing old logs . . ."+Color.RESET)
        logger.clear_old_logs()
    
    except Exception as e:
        logging.error(type(e).__name__+": "+str(e))
        raise type(e)(str(e))