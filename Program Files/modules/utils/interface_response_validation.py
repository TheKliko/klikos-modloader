import os


def integer(data: str, min: int = None, max: int = None) -> bool:
    """
    Check if given data is an integer
    
    :param data: The data to validate
    :param min: (optional) The minimum value that the integer must be. Default: None
    :param max: (optional) The maximum value that the integer may be. Default: None
    
    :type data: str
    :type min: int
    :type max: int
    
    :rtype bool
    :return True if the given data is an integer, otherwise False
    """

    try:
        data = int(data)
    
    except:
        return False
    
    if min and max and data >= min and data <= max:
        return True
    
    elif min and not max and data >= min:
        return True
    
    elif not min and max and data <= max:
        return True
    
    elif not min and not max:
        return True

    else:
        return False

def boolean(data: str) -> tuple[bool, bool | str]:
    """
    Check if given data is a boolean
    
    :param data: The data to validate
    
    :type data: str
    
    :rtype tuple
    :return (True, True) if the given data is True, (True, False) if the given data is False, otherwise (False, 'NOPE')
    """

    TRUE: list[str] = [
        'true',
        'y',
        'yes'
    ]
    FALSE: list[str] = [
        'false',
        'n',
        'no'
    ]
    
    if data.lower() in TRUE:
        return (True, True)
    
    elif data.lower() in FALSE:
        return (True, False)
    
    else:
        return (False, 'NOPE')


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()