"""# variables.py

variables.py is a module used in Kliko's modloader,
it's purpose is to store variables used by different modules.
"""


import logging
import os
from typing import Any


variables: dict = {}


def get(name: str) -> Any:
    """Returns the value of a stored variable

    :param name: the name of the stored variable
    :type name: str
    :rtype Any
    :return The value of the stored variable if the given variable exists, otherwise None
    """

    try:
        value = variables[name]
        return value
    
    except KeyError as e:
        logging.error(f'A {type(e).__name__} occured while reading stored variables')
        logging.debug(f'Failed to find variable: "{name}"')

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured while reading stored variables')
        logging.debug(f'{type(e).__name__}: {str(e)}')
    
    return None
    

def set(name: str, value: Any) -> None:
    """Stores a value to a given variable name

    :param name: the name of the variable to be stored
    :param value: the value of the variable to be stored
    :type name: str
    :type value: Any
    :rtype None
    :return None
    """

    variables[name] = value
    return None


def get_silent(name: str) -> Any:
    """Returns the value of a stored variable without logging errors

    :param name: the name of the stored variable
    :type name: str
    :rtype Any
    :return The value of the stored variable if the given variable exists, otherwise None
    """

    try:
        value = variables[name]
        return value

    except:
        pass
    
    return None


def debug_print() -> None:
    print(variables)


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()