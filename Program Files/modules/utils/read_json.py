"""# read_json.py

read_json.py is a module used in Kliko's modloader,
it's purpose is to handle read interactions with json files.
"""


import json
import logging
import os

from typing import Any


def complete(filepath: str) -> dict | None:
    """Function called to read the entirety of a given json file

    :param filepath: the path to the json file
    :type filepath: str
    :rtype dict | None
    :return The config of the given json file if it exists, otherwise None
    """

    try:
        with open(filepath, 'r') as file:
            config = json.load(file)
            file.close()
        return config

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    
    return None


def value(filepath: str, key: str) -> Any:
    """Function called to read a specific value from a given json file

    :param filepath: the path to the json file
    :param key: the key from which the value will be returned
    :type filepath: str
    :type key: str
    :rtype Any
    :return The value of a key within the given json file if it exists, otherwise None
    """

    try:
        with open(filepath, 'r') as file:
            config = json.load(file)
            file.close()
        value = config[key]
        return value
    
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