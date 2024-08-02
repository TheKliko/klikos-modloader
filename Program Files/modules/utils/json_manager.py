import json
import logging
import os
from typing import Any

from modules.utils import filesystem


class JsonError(Exception):
    f"""Exception raised by {os.path.basename(__file__)}"""
    pass


def read(path: str, key: str = None) -> dict | Any:
    """
    Return the data (entire file or a specific value) in a .json file
    
    :param path: The path to the .json file
    :param key: (optional) Specify a json key to get a specific value. Default: None
    
    :type path: str
    :type key: str
    
    :rtype dict | Any
    :return The complete data or specific value of a .json file
    """

    logging.info(f'Reading {os.path.basename(path)}')
    filesystem.validate(path)

    with open(path, 'r') as file:
        config: dict = json.load(file)
        file.close()
    
    if not key:
        return config
    
    elif isinstance(key, str):
        if key in config.keys():
            return config[key]
        
        else:
            raise JsonError(f'Could not find key \'{key}\' in {os.path.basename(path)}')


def update(path: str, key: str, value: Any) -> None:
    """
    Update a value in a .json file
    
    :param path: The path to the .json file
    :param key: The key to update
    :param value: The new value
    
    :type path: str
    :type key: str
    :type value: Any
    
    :rtype None
    :return None
    """

    logging.info(f'Updating {os.path.basename(path)}')
    filesystem.validate(path)

    with open(path, 'r') as file:
        config: dict = json.load(file)
        file.close()
    
    config[key] = value

    with open(path, 'w') as file:
        json.dump(config, file, indent=4)
        file.close()


def remove(path: str, key: Any) -> None:
    """
    Remove a key-value pair from a .json file
    
    :param path: The path to the .json file
    :param key: The key to remove
    
    :type path: str
    :type key: Any
    
    :rtype None
    :return None
    """
    
    logging.info(f'Removing key-value pair from {os.path.basename(path)}')
    filesystem.validate(path)

    with open(path, 'r') as file:
        config: dict = json.load(file)
        file.close()
    
    if key in config.keys():
        config.pop(key)

    with open(path, 'w') as file:
        json.dump(config, file, indent=4)
        file.close()


def write(path: str, config: dict) -> None:
    """
    Overwrite a .json file or create a new one
    
    :param path: The path to the .json file
    :param config: The config to write
    
    :type path: str
    :type config: dict
    
    :rtype None
    :return None
    """

    logging.info(f'Writing {os.path.basename(path)}')
    with open(path, 'w') as file:
        json.dump(config, file, indent=4)
        file.close()


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()