import os
import json
import logging

from modules.json_handler import get_json_value_from_file as get_variable
from modules.json_handler import update_json as set_variable

from main import root_directory

temporary_directory: str = os.path.join(root_directory, 'Program Files', 'temporary')
variables_file: str = os.path.join(temporary_directory, 'variables.json')


def create_file() -> None:
    logging.info(f'Creating temporary file: {os.path.basename(variables_file)}')
    try:
        os.makedirs(name=temporary_directory, exist_ok=True)
        with open(variables_file, 'w') as file:
            file.write('{}')
            file.close()
    
    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def get(name: str):
    try:
        value = get_variable(
            path=variables_file,
            key=name
        )
        return value
    
    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def set(name: str, value):
    try:
        set_variable(
            path=variables_file,
            key=name,
            value=value
        )
    
    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()