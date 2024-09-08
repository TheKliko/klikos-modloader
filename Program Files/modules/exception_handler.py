import logging

from modules.other.hyperlinks import Hyperlink
from modules.interface import Interface, Color, foreground, clear, Style, Input, Alignment


def run(exception) -> None:
    logging.error(f'[{type(exception).__name__}] {str(exception)}')
    
    interface = Interface(
        section='!!! Something went wrong !!!'
    )

    interface.add_line(f'[{type(exception).__name__}] {str(exception)}', color=Color.ERROR)
    interface.add_line('-', is_divider = True)

    interface.add_line('If you need any help, please visit one of the following URLs')
    interface.add_line(' ', is_divider=True)
    interface.add_line('Discord:')
    interface.add_line(Hyperlink.DISCORD, color=Color.URL, style=Style.UNDERLINE)
    interface.add_line(' ', is_divider=True)
    interface.add_line('GitHub:')
    interface.add_line(Hyperlink.GITHUB, color=Color.URL, style=Style.UNDERLINE)
    interface.add_line(' ', is_divider=True)
    interface.add_line('Website:')
    interface.add_line(Hyperlink.WEBSITE, color=Color.URL, style=Style.UNDERLINE)
    interface.add_line('-', is_divider = True)

    interface.get_input('Press ENTER to exit . . .', text_color=Color.BORDER, input_style=Style.HIDDEN)