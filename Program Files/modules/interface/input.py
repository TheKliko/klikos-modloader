from typing import Literal

from .foreground import foreground
from .styles import Style


DEFAULT: str = '\033[0m'


class Input:
    @classmethod
    def get(self,  # This looks so goofy
                 text: str,
                 text_color: str = '',
                 text_style: Literal[
                     Style.BOLD,
                     Style.ITALIC,
                     Style.UNDERLINE,
                     Style.DOUBLE_UNDERLINE,
                     Style.OVERLINE,
                     Style.STRIKETHROUGH,
                     Style.HIDDEN,
                     Style.DIM,
                     Style.BLINK
                     ] = '',
                 input_color: str = '',
                 input_style: Literal[
                     Style.BOLD,
                     Style.ITALIC,
                     Style.UNDERLINE,
                     Style.DOUBLE_UNDERLINE,
                     Style.OVERLINE,
                     Style.STRIKETHROUGH,
                     Style.HIDDEN,
                     Style.DIM,
                     Style.BLINK
                     ] = '',
                indent: int = 0) -> str:

        if text_color != '':
            text_color = foreground(text_color)
        if input_color != '':
            input_color = foreground(input_color)
        response: str = input(f'{' '*indent}{text_color}{text_style}{text}{DEFAULT}{input_color}{input_style}')
        print(DEFAULT, end='')
        
        return response