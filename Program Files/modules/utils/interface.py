"""# interface.py

interface.py is a module used in Kliko's modloader,
it's purpose is to display the user interface.
"""


import ctypes
import os

from modules.utils import variables


# PROGRAM_NAME: str = variables.get('project_name')
# PROGRAM_VERSION: str = variables.get('project_description')
# PROGRAM_DESCRIPTION: str = variables.get('project_description')
# PROGRAM_AUTHOR: str = variables.get('project_author')


# Clear terminal using https://stackoverflow.com/a/684344
def clear() -> None:
    """Function called to clear the terminal"""
    os.system('cls' if os.name=='nt' else 'clear')
    return None


def open(section: str | None = None) -> None:
    """Function called to generate the default interface
    
    :param section: (optional) the name of the opened section. Default: None
    :type section: str | None
    """

    PROGRAM_DESCRIPTION: str = variables.get('project_description')
    PROGRAM_NAME: str = variables.get('project_name')
    program_version: str = variables.get('version')
    if not program_version:
        program_version = 'ersion unknown'

    clear()
    print(f'{PROGRAM_NAME} (v{program_version})')
    print(f'{PROGRAM_DESCRIPTION}')
    print()

    if section:
        # print(f'--[ {section} ]--')
        print(f'  [ {section} ]')
        # print(f'\u2919 {section} \u291A')
        print()

    return None


def text(message: str | list, spacing: int = 1) -> None:
    """Prints a message to the interface
    
    :param message: The message, or messages, to print to the interface
    :type message: str | list
    :param spacing: (optional) the amount of empty lines to print before printing the message. Default: 1
    :type spacing: int
    """

    for i in range(spacing):
        print()

    if type(message) is list:
        for line in message:
            print(line)
    else:  # type(message) is str
        print(message)

    return None

def confirm(prompt: str, spacing: int = 1) -> bool:
    """Prints a confirmation prompt to the interface
    
    :param prompt: The prompt to print to the interface
    :type prompt: str
    :param spacing: (optional) the amount of empty lines to print before printing the message. Default: 1
    :type spacing: int
    :rtype bool
    :return True if the user confirms, otherwise False
    """

    CONFIRM: list = ['y', 'yes', 'true']
    DENY: list = ['n', 'no', 'false']

    for i in range(spacing):
        print()

    while True:
        print(f'{prompt} [Y/N]')
        response = input('Response: ')
        if response in CONFIRM:
            value = True
            break
        if response in DENY:
            value = False
            break
        else:
            text(
                [
                    'Invalid response!',
                    f'Accepted response are {CONFIRM} OR {DENY}'
                ]
            )
            print()

    return value


def select(options: list[str], prompt: str = 'Select an option', spacing: int = 1) -> tuple[int, str]:
    """Prints a selection prompt to the interface

    :param prompt: The prompt to print to the interface
    :param options: The options that the user can choose from
    :param spacing: (optional) the amount of empty lines to print before printing the message. Default: 1
    :type prompt: str
    :type options: list[str]
    :type spacing: int
    :rtype tuple(int, str)
    :return A tuple containing the response, formatted as (index, value)
    """

    SELECTED_INDICATOR: str = variables.get('selected_item_indicator')

    for i in range(spacing):
        print()
    
    print(prompt)
    for i, option in enumerate(options):
        print(f'[{i+1}]: {option}')
    
    while True:
        print()
        response = input('response: ')
        try:
            if int(response)-1 in range(len(options)):
                if SELECTED_INDICATOR in str(options[int(response)-1]):
                    options[(int(response)-1)] = options[(int(response)-1)][:-len(SELECTED_INDICATOR)]
                values = (int(response)-1), options[(int(response)-1)]
                return values
        except:
            pass
        
        print()
        print(f'Invalid response: "{response}"')
        print(f'Accepted responses are: [1-{len(options)}]')


def select_number(min: int = None, max: int = None, prompt: str = 'Select an option', spacing: int = 1) -> int:
    """Prints a number selection prompt to the interface

    :param min: (optional) The lowest number that the user can choose from
    :param max: (optional) The highest number that the user can choose from
    :param prompt: The prompt to print to the interface
    :param spacing: (optional) the amount of empty lines to print before printing the message. Default: 1
    :type min: int
    :type max: int
    :type prompt: str
    :type spacing: int
    :rtype int
    :return The selected number
    """

    for i in range(spacing):
        print()

    if min is None and max is None:
        print(f'{prompt}')
    elif min is not None and max is None:
        print(f'{prompt} [>={min}]')
    elif min is None and max is not None:
        print(f'{prompt} [<={max}]')
    else:  # min is not None and max is not None
        print(f'{prompt} [{min}-{max}]')
    
    while True:
        print()
        response = input('response: ')
        try:
            value = int(response)
            if min is not None:
                if value < min:
                    raise Exception
            if max is not None:
                if value > max:
                    raise Exception
            return value
        except:
            pass
        
        print()
        print(f'Invalid response: "{response}"')


def prompt(prompt: str | list[str], restrict_characters: list[str] = None, restrict_responses: list[str]= None, spacing: int = 1, response_spacing: int = 1) -> str:
    """Prints an input prompt to the interface

    :param prompt: The prompt to print to the interface
    :param restrict_characters: (optional) characters that may not be included in the response. Default: None
    :param restrict_responses: (optional) responses that may not be returned. Default: None
    :param spacing: (optional) the amount of empty lines to print before printing the message. Default: 1
    :param spacing: (optional) the amount of empty lines to print between the prompt and response. Default: 1
    :type prompt: str
    :type restrict_characters: list[str]
    :type restrict_responses: list[str]
    :type spacing: int
    :type response_spacing: int
    :rtype tuple(int, str)
    :return A string containing the response
    """

    for i in range(spacing):
        print()
    
    if type(prompt) is list:
        for line in prompt:
            print(line)
    else:  # type(message) is str
        print(prompt)
    
    while True:
        for i in range(response_spacing):
            print()
        response = input('response: ')
        
        if restrict_characters and any(char in response for char in restrict_characters):
            print(f'Invalid response: "{response}"')
            print(f'Response may not include the following character(s): {restrict_characters}')

        elif restrict_responses and any(char in response for char in restrict_responses):
            print(f'Invalid response: "{response}"')
            print(f'Response may not one of be the following item(s): {restrict_responses}')

        else:
            return response


def minimize() -> None:
    """Function called to minimize the terminal"""
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()