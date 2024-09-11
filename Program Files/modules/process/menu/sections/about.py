from modules import interface
from modules.other.licenses import LICENSES
from modules.other.hyperlinks import Hyperlink


def show(window: interface.Interface) -> str:
    while True:
        window.change_section_description()
        window.reset()

        options: list = [
            'Go Back',
            'View License',
            'Help'
        ]
        for i, option in enumerate(options, start=1):
            window.add_line(f'[{i}]:{f" " if i < 10 else ""} {option}')
        window.add_divider()

        bad_input: bool = False
        while True:
            response: str = window.get_input('Response: ')
            try:
                i = int(response)
                if i > 0 and i <= len(options):
                    if i == 1:
                        return 'home'
                    
                    elif i == 2:
                        show_license(window)
                    
                    elif i == 3:
                        show_help(window)

                    break
            except:
                pass

            if bad_input != False:
                window.remove_last(3)
            window.add_line(f'Invalid response: "{response}"')
            window.add_line(f'Accepted answers are: [1-{len(options)}]')
            window.add_divider()
            bad_input = True
            window._on_update()


def show_license(window: interface.Interface) -> None:
    window.change_section_description(' > License')
    window.reset()

    try:
        url_decorator: str = f'{interface.foreground(interface.Color.URL)}{interface.Style.UNDERLINE}'
        for license in LICENSES:
            window.add_line(f'Name: {license.get('name', None)}')
            window.add_line(f'Type: {license.get('type', None)}')
            window.add_line(f'URL: {url_decorator}{license.get('url', None)}{interface.Color.DEFAULT}')
            if license != LICENSES[-1]:
                window.add_line(' ')
        window.add_divider()
        window.get_input('Press ENTER to return . . .')

    except Exception as e:
        window.add_line('Section failed to load!', color=interface.Color.WARNING)
        window.add_line(f'[{type(e).__name__}]: {str(e)}', color=interface.Color.ERROR)
        window.add_divider()
        window.get_input('Press ENTER to return . . .')


def show_help(window: interface.Interface) -> None:
    window.change_section_description(' > Help')
    window.reset()

    try:
        url_decorator: str = f'{interface.foreground(interface.Color.URL)}{interface.Style.UNDERLINE}'
        
        window.add_line(f'\u2022 Discord: {url_decorator}{Hyperlink.DISCORD}{interface.Color.DEFAULT}')
        window.add_line(f'\u2022 GitHub: {url_decorator}{Hyperlink.GITHUB}{interface.Color.DEFAULT}')
        window.add_line(f'\u2022 Website: {url_decorator}{Hyperlink.WEBSITE}{interface.Color.DEFAULT}')
        window.add_divider()
        window.get_input('Press ENTER to return . . .')

    except Exception as e:
        window.add_line('Section failed to load!', color=interface.Color.WARNING)
        window.add_line(f'[{type(e).__name__}]: {str(e)}', color=interface.Color.ERROR)
        window.add_divider()
        window.get_input('Press ENTER to return . . .')