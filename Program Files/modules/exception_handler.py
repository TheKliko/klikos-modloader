import logging
import os

from modules.interface import Color, clear


def run(exception: Exception) -> None:
    if type(exception) == SystemExit:
        logging.info("No errors! Shutting down . . .")
        return
    
    logging.error(type(exception).__name__+": "+str(exception))
    clear()
    print(Color.ERROR+"ERROR: "+type(exception).__name__+"!")
    print(Color.WARNING+str(exception))
    print(Color.RESET)
    input("Press ENTER to close . . .")