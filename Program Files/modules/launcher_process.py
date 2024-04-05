import os
import logging
import inspect
import subprocess
import multiprocessing

from modules.roblox_update_handler import check_for_update
from modules.basic_functions import open_console



def launcher(version_directory: str) -> None:
    logging.info(f'Starting {inspect.stack()[0][3]}...')

    open_console()
    check_for_update()

    process = multiprocessing.Process(target=launch_roblox, args=(version_directory,))
    process.start()

def launch_roblox(version_directory: str) -> None:
    from modules.roblox_update_handler import latest_roblox_version

    logging.info(f'Launching Roblox {latest_roblox_version}')

    try:
        command: str = f'{os.path.join(version_directory, latest_roblox_version, 'RobloxPlayerBeta.exe')}'
        subprocess.run(command)
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