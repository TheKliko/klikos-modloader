import logging
import os
import time

from modules.interface import Print, Color
from modules.utils import filesystem
from modules.other.paths import Directory

def start() -> None:
    Print('Initializing logger . . .', color=Color.INITALIZE)

    log_directory: str = Directory.LOGS
    log_filename: str = f'log_{time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())}.log'
    log_filepath: str = os.path.join(log_directory, log_filename)

    filesystem.verify(log_directory, create_missing_directories=True)

    logging.basicConfig(
        filename=log_filepath,
        level=logging.DEBUG,
        format='[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(filename)s.%(funcName)s(@line_%(lineno)d)]: %(message)s',
        datefmt='%Y-%m-%d_%H:%M:%S',
        encoding='utf-8'
    )
    logging.info(f'Writing logs to: {log_filename}')

    logging.getLogger('PIL').setLevel(logging.ERROR)