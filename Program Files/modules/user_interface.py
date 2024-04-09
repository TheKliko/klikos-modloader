import os

from modules.json_handler import get_json_value_from_input

from modules import variables

config_json = variables.get(name='config_json')
program_name: str = get_json_value_from_input(config=config_json, key='title')
program_version: str = get_json_value_from_input(config=config_json, key='version')
program_description: str = get_json_value_from_input(config=config_json, key='description')



def open() -> None:
    print(f'{program_name} (v{program_version})')
    print(f'{program_description}')

def confirmation_prompt(prompt: str) -> bool:
    confirm: list[str] = ['y', 'yes']
    deny: list[str] = ['n', 'no']

    print()
    while True:
        print(f'{prompt} [Y/N]')
        response = input('response:')
        if response.lower() in confirm:
            return True
        if response.lower() in deny:
            return False
        else:
            print(f'Response \'{response}\' is invalid!')
            print()
            print(f'Accepted responses are: {confirm} OR {deny}')

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

def press_enter_to(message: str, spacing: int = 1) -> None:
    try:
        for i in range(spacing):
            print()
    except:
        pass
    input(f'Press ENTER to {message}')



def main():
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()