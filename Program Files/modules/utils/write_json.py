"""# write_json.py

write_json.py is a module used in Kliko's modloader,
it's purpose is to handle write interactions with json files.
"""


import json
import logging
import os

from typing import Any


def complete(filepath: str, config: dict) -> None:
    """Function called to overwrite a given json file

    :param filepath: the path to the json file
    :param config: the config to be written
    :type filepath: str
    :type config: dict
    :rtype None
    :return None
    """

    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as file:
            json.dump(config, file, indent=4)
            file.close()
        return None

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    
    return None


def value(filepath: str, key: str, value: Any) -> None:
    """Function called to overwrite a specific value from a given json file

    :param filepath: the path to the json file
    :param key: the key to be written
    :param value: the value of the given key
    :type filepath: str
    :type key: str
    :type config: dict
    :rtype None
    :return None
    """

    try:
        with open(filepath, 'r') as file:
            config = json.load(file)
            file.close()
        config[key] = value
        with open(filepath, 'w') as file:
            json.dump(config, file, indent=4)
            file.close()
    
    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')

    return value


def rename_key(filepath: str, key: str, name: str) -> None:
    """Function called to rename a specific key from a given json file

    :param filepath: the path to the json file
    :param key: the key to be renamed
    :param name: the name that the key will be renamed to
    :type filepath: str
    :type key: str
    :type name: str
    :rtype None
    :return None
    """

    with open(filepath, 'r') as file:
        config:dict = json.load(file)
        file.close()
    
    if key in config:
        config[name] = config.pop(key)
        with open(filepath, 'w') as file:
            json.dump(config, file, indent=4)


def remove_key(filepath: str, key: str) -> None:
    """Function called to remove a specific key and it's value from a given json file

    :param filepath: the path to the json file
    :param key: the key to be removed
    :type filepath: str
    :type key: str
    :rtype None
    :return None
    """

    with open(filepath, 'r') as file:
        config:dict = json.load(file)
        file.close()
    
    if key in config:
        del config[key]
        with open(filepath, 'w') as file:
            json.dump(config, file, indent=4)


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()