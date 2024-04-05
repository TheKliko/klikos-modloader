import os
import sys
import time
import logging
import shutil

from modules.json_handler import get_json_value_from_input



def open_console() -> None:
    from modules.initialization import config_json
    program_name: str = get_json_value_from_input(config=config_json, key='title')
    program_version: str = get_json_value_from_input(config=config_json, key='version')
    program_description: str = get_json_value_from_input(config=config_json, key='description')

    print(f'{program_name} (v{program_version})')
    print(f'{program_description}')
    print()

def confirmation_prompt(prompt: str) -> bool:
    while True:
        print(f'{prompt} [Y/N]')
        response = input('response:')
        if response.lower() in ['y','yes']:
            return True
        if response.lower() in ['n','no']:
            return False

# def continuation_prompt(prompt: str) -> None:
#     while True:
#         print(f'{prompt}')
#         response = input('press ENTER to continue')

def copy_directory(source: str, destination: str) -> None:
    try:
        shutil.copytree(src=source, dst=destination, dirs_exist_ok=True)
    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def terminate(timer: int) -> None:
    logging.info('Terminating program')
    for i in range(timer,0, -1):
        print(f'Terminating program in {i}', end='\r')
        time.sleep(1)
    sys.exit()

def main():
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()