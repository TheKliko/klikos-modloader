import os
import sys
import logging
import shutil
import time

from modules.directory_functions import remove_directory

from main import root_directory
temporary_directory: str = os.path.join(root_directory, 'Program Files', 'temporary')


def start(timer: int | None = None) -> None:
    logging.debug(f'Starting {os.path.splitext(os.path.basename(__file__))[0]}')
    remove_temporary_files()
    if timer is None:
        timer = 5
    terminate(timer=timer)

def terminate(timer: int) -> None:
    logging.info(f'Terminating program')
    for i in range(timer,0, -1):
        print(f'Terminating program in {i}', end='\r')
        time.sleep(1)
    sys.exit()

def remove_temporary_files() -> None:
    try:
        logging.debug(f'Removing temporary files')
        remove_directory(
            source=temporary_directory,
            name=os.path.join(os.path.basename(os.path.dirname(temporary_directory)), os.path.basename(temporary_directory))
        )
    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None



def main():
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()