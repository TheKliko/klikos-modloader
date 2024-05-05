import os
import logging

from modules.json_handler import get_json_value_from_input

from modules import variables

config_json = variables.get(name='config_json')
program_name: str = get_json_value_from_input(config=config_json, key='title')
program_version: str = get_json_value_from_input(config=config_json, key='version')
program_description: str = get_json_value_from_input(config=config_json, key='description')


def open(section: str | None = None) -> None:
    print(f'{program_name} (v{program_version})')
    print(f'{program_description}')
    if section:
        print()
        print(f'-- {section} --')
    return None

def print_message(message: str | list[str], spacing: int = 1) -> None:
    try:
        for i in range(spacing):
            print()
    except:
        pass

    if type(message) == str:
        print(message)
    else: # type(message) == list[str]
        for item in message:
            print(item)
    return None

def print_message_replace(message: str, spacing: int = 0):
    try:
        for i in range(spacing):
            print()
    except:
        pass

    print(message, end='\r')
    return None

def print_newline(spacing: int = 1):
    try:
        for i in range(spacing):
            print()
    except:
        pass
    return None

def selection_prompt(prompt: str, options: list[str], spacing: int = 1, title: bool = False):
    try:
        for i in range(spacing):
            print()
    except:
        pass

    try:
        print(prompt)
        if title == True:
            for i, option in enumerate(options):
                print(f'[{i+1}]: {option.title()}')
        else:
            for i, option in enumerate(options):
                print(f'[{i+1}]: {option}')
        print_newline()
        while True:
            response = input('response: ')
            try:
                if (int(response)-1) in range(len(options)):
                    if '  <- Selected' in options[(int(response)-1)]:
                        options[(int(response)-1)] = options[(int(response)-1)][:-len(' <- Selected')]
                    values = (int(response)-1), options[(int(response)-1)]
                    return values
            except:
                pass
            print()
            print(f'Response \'{response}\' is invalid!')
            print(f'Accepted responses are: [1-{len(options)}]')
            print()
            

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def confirmation_prompt(prompt: str, message: str | None = None, spacing: int = 1) -> bool:
    confirm: list[str] = ['y', 'yes', 'true']
    deny: list[str] = ['n', 'no', 'false']

    try:
        for i in range(spacing):
            print()
    except:
        pass

    while True:
        print(f'{prompt} [Y/N]')
        if message:
            print(f'{message}')
        response: str = str(input('response: '))
        if response.lower() in confirm:
            return True
        if response.lower() in deny:
            return False
        else:
            print(f'Response \'{response}\' is invalid!')
            print()
            print(f'Accepted responses are: {confirm} OR {deny}')

def press_enter_to(message: str, spacing: int = 1) -> None:
    try:
        for i in range(spacing):
            print()
    except:
        pass
    input(f'Press ENTER to {message}')
    return None

# Clear terminal using https://stackoverflow.com/a/684344
def clear_console() -> None:
    os.system('cls' if os.name=='nt' else 'clear')
    return None



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()