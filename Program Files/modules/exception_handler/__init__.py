import logging

from modules.interface import Interface, Color, foreground, clear, Style, Input, Alignment


def run(exception) -> None:
    logging.error(f'[{type(exception).__name__}] {str(exception)}')
    
    interface = Interface(
        section='!!! Something went wrong !!!'
    )

    interface.add_line(f'[{type(exception).__name__}] {str(exception)}', color=Color.ERROR)
    interface.add_line('-', is_divider = True)

    interface.get_input('Press ENTER to exit . . .', text_color=Color.BORDER, input_style=Style.HIDDEN)