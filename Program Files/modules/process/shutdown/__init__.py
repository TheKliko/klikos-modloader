import logging
import sys

from .exceptions import *


def run() -> None:
    logging.info('Shutting down . . .')
    sys.exit()