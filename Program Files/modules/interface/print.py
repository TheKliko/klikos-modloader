from typing import Literal

from .foreground import foreground
from .styles import Style


DEFAULT: str = '\033[0m'


class Print:
    def __init__(self,  # This looks so goofy
                 text: str,
                 color: str = '',
                 style: Literal[
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
                indent: int = 0) -> None:

        if color != '':
            color = foreground(color)
        print(f'{' '*indent}{color}{style}{text}{DEFAULT}')