import os
import sys
import logging
import shutil
import multiprocessing
import ctypes
from packages import psutil
import time
from modules.directory_functions import remove_directory
from modules import user_interface as interface
from modules import rich_presence

from main import root_directory

temporary_directory: str = os.path.join(root_directory, 'Program Files', 'temporary')


def start(timer: int = 5) -> None:
    logging.debug(f'Starting {os.path.splitext(os.path.basename(__file__))[0]}')
    if roblox_is_running():
        interface.print_message('Program will terminate when exiting Roblox')
        time.sleep(3)
        ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )
        while roblox_is_running():
            time.sleep(1)
    else:
        for i in range(timer,0, -1):
            interface.print_message_replace(f'Terminating program in {i}')
            time.sleep(1)
    remove_temporary_files()
    terminate()

def terminate() -> None:
    logging.info(f'Terminating program')
    try:
        rich_presence.stop()
    except:
        pass
    sys.exit()

def remove_temporary_files() -> None:
    try:
        logging.warning(f'Removing temporary files')
        remove_directory(
            source=temporary_directory,
            name=os.path.join(os.path.basename(os.path.dirname(temporary_directory)), os.path.basename(temporary_directory))
        )
    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def roblox_is_running() -> bool:
    for proc in psutil.process_iter():
        try:
            if "RobloxPlayerBeta.exe" in proc.name():
                return True
        except:
            pass
    return False



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()