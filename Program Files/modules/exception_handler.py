import logging

from modules.other.hyperlinks import Hyperlink
from modules.interface import Interface, Color, Style


def run(exception) -> None:
    logging.error(f'[{type(exception).__name__}] {str(exception)}')
    
    interface = Interface(
        section='\u26a0  Something went wrong!',
        color=Color.WARNING
    )

    interface.add_line(f'[{type(exception).__name__}] {str(exception)}', color=Color.ERROR)
    interface.add_divider()

    interface.add_line('If you need any help, please visit one of the following URLs')
    interface.add_line(' ')
    interface.add_line('Discord:')
    interface.add_line(Hyperlink.DISCORD, color=Color.URL, style=Style.UNDERLINE)
    interface.add_line(' ')
    interface.add_line('GitHub:')
    interface.add_line(Hyperlink.GITHUB, color=Color.URL, style=Style.UNDERLINE)
    interface.add_line(' ')
    interface.add_line('Website:')
    interface.add_line(Hyperlink.WEBSITE, color=Color.URL, style=Style.UNDERLINE)
    interface.add_divider()

    interface.get_input('Press ENTER to exit . . .', input_style=Style.HIDDEN)