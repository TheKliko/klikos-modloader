import ctypes
import os

from modules.utils import variables


INTERFACE_WIDTH: int = 72
TERMINAL_WIDTH = os.get_terminal_size().columns


class Aligntment:
    left: str = 'LEFT'
    right: str = 'RIGHT'
    center: str = 'CENTER'


def clear() -> None:
    """Clear the terminal"""
    os.system('cls' if os.name=='nt' else 'clear')


def open(section: str | list[str] = None) -> None:
    """
    Open the interface on a given section
    
    :param section: the name of the opened section
    
    :type section: str | list[str]
    
    :rtype None
    :return None
    """

    project_data: dict = variables.get('project_data')
    project_name: str = project_data['name']
    project_version: str = project_data['version']
    project_description: str = project_data['description']

    clear()
    print()
    divider()
    print(f'{f'| {f'{project_name} - {project_version}':^{INTERFACE_WIDTH}} |':^{TERMINAL_WIDTH}}')
    print(f'{f'| {project_description:^{INTERFACE_WIDTH}} |':^{TERMINAL_WIDTH}}')

    if section:
        divider()

        if type(section) == str:
                if len(section) <= INTERFACE_WIDTH:
                    print(f'{f'| {section:^{INTERFACE_WIDTH}} |':^{TERMINAL_WIDTH}}')
                
                else:
                    print_wrapped(textwrap(section), '^')
        
        elif type(section) == list:
            for line in section:
                if len(line) <= INTERFACE_WIDTH:
                    print(f'{f'| {line:^{INTERFACE_WIDTH}} |':^{TERMINAL_WIDTH}}')
                
                else:
                    print_wrapped(textwrap(line), '^')

    divider()


def text(content: str | list[str], alignment: str = Aligntment.left) -> None:
    """
    Print text to the interface
    
    :param content: The content to print to the interface
    :param alignment: (optional) The name of the opened section. Default: Alignment.left
    
    :type content: str | list[str]
    :type aligntment: str
    
    :rtype None
    :return None
    """

    ALIGNMENT_MAP: dict = {
        Aligntment.left: '<',
        Aligntment.center: '^',
        Aligntment.right: '>'
    }
    alignment = ALIGNMENT_MAP.get(alignment.upper(), '<')
    
    if isinstance(content, str):
        if len(content) <= INTERFACE_WIDTH:
            print(f'{f'| {content:{alignment}{INTERFACE_WIDTH}} |':^{TERMINAL_WIDTH}}')
        
        else:
            print_wrapped(textwrap(content), alignment)
    
    elif isinstance(content, list):
        for line in content:
            if len(line) <= INTERFACE_WIDTH:
                print(f'{f'| {line:{alignment}{INTERFACE_WIDTH}} |':^{TERMINAL_WIDTH}}')

            else:
                print_wrapped(textwrap(line), alignment)


def prompt(content: str = 'Response: ') -> str:
    """
    Print a text prompt to the interface, returns the given response
    
    :param content: The prompt to print to the interface
    
    :type content: str
    
    :rtype str
    :return The given response
    """

    print()
    response = input(f'{'':<{(TERMINAL_WIDTH - INTERFACE_WIDTH) / 2}}{content}')
    return response


def newline(count: int = 1) -> None:
    """Print whitespace to the terminal"""
    for i in range(count):
        print(f'{f'| {'':^{INTERFACE_WIDTH}} |':^{TERMINAL_WIDTH}}')


def divider() -> None:
    """Print a divider line to the terminal"""
    print(f'{f'+-{'':-^{INTERFACE_WIDTH}}-+':^{TERMINAL_WIDTH}}')


def minimize() -> None:
    """Minimize the terminal"""
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)


def textwrap(content: str, length: int = INTERFACE_WIDTH) -> list:
    """Helper function. Return wrapped text"""
    words = content.split()
    current_line = words[0]

    result = []
    for word in words[1:]:
        if len(current_line) + len(f' {word}') < length:
            current_line += f' {word}'
        else:
            result.append(current_line)
            current_line = word
    result.append(current_line)
    return result

def print_wrapped(content: list[str], aligntment) -> None:
    """Helper function. Print wrapped text"""
    for line in content:
        print(f'{f'| {line:{aligntment}{INTERFACE_WIDTH}} |':^{TERMINAL_WIDTH}}')


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()