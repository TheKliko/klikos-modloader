import os
from typing import Any

variables: dict = {}


class VariableError(Exception):
    f"""Exception raised by {os.path.basename(__file__)}"""
    pass


def set(key: str, value: Any, overwrite: bool = True) -> None:
    """
    Set the value of a variable to be used across different modules.

    :param key: The name of the variable
    :param value: The value of the variable
    :param overwrite: (optional) Whether existing variables may be overwritten. (default = True)
    
    :type key: str
    :type value: Any
    :type value: bool

    :rtype None
    :return Nothing
    """

    if key in variables.keys() and overwrite == False:
        raise VariableError(f'Variable already exists: {key}')
    
    variables[key] = value


def get(key: str, silent: bool = True) -> Any:
    """
    Get the value of a stored variable if it exists, otherwise raise a VariableError if silent == False.

    :param key: The name of the variable
    :param silent: (optional) Doesn't raise an error if True (default = True)

    :type key: str
    :type silent: bool

    :rtype Any
    :return The value of the requested variable
    """

    if key in variables.keys():
        return variables[key]
    
    elif silent:
        return None
    
    raise VariableError(f'Variable not found: {key}')


def remove(key: str) -> None:
    """
    Remove a stored variable if it exists.

    :param key: The name of the variable
    :type key: str

    :rtype None
    :return Nothing
    """

    if key in variables.keys():
        variables.pop(key)


def debug() -> None:
    """Print all stored variables"""
    
    print(variables)
    input()


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()