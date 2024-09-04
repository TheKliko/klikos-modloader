import shutil
from typing import Literal, Any

from modules.other.project import Project

from .foreground import foreground
from .colors import Color
from .styles import Style
from .aligntment import Alignment
from .background import background
from .clear import clear


class Interface:
    terminal_size = shutil.get_terminal_size()
    terminal_width: int = terminal_size.columns
    terminal_height: int = terminal_size.lines

    width: int = terminal_width - 48
    
    BORDER_COLOR: str = foreground(Color.BORDER)
    DEFAULT: str = '\033[0m'
    BACKGROUND: str = '#1f1f1f'

    data: list[dict[str, Any]] = []


    def __init__(
            self,
            section: str,
            description: str = None,
            color: str = Color.SECTION_TITLE,
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
            alignment: Literal[
                Alignment.LEFT,
                Alignment.RIGHT,
                Alignment.CENTER
            ] = Alignment.LEFT,
            background_color: str = None
        ) -> None:

        background(background_color or self.BACKGROUND)

        title_color = foreground(Color.TITLE)

        if color != '':
            color = foreground(color)
        else:
            color = self.DEFAULT

        self.data = []
        
        self.data.append(
            {
                'gap': '-',
                'type': 'divider',
                'color': self.BORDER_COLOR,
            }
        )
        self.data.append(
            {
                'data': Project.NAME,
                'color': title_color,
                'alignment': Alignment.LEFT
            }
        )
        self.data.append(
            {
                'data': f'Version: {Project.VERSION}',
                'color': title_color,
                'alignment': Alignment.LEFT
            }
        )


        self.data.append(
            {
                'gap': '-',
                'type': 'divider',
                'color': self.BORDER_COLOR,
            }
        )
        self.data.append(
            {
                'type': 'divider',
                'color': self.BORDER_COLOR,
            }
        )
        self.data.append(
            {
                'data': section,
                'color': color,
                'alignment': alignment,
                'style': style
            }
        )
        if description != None:
            self.data.append(
                {
                    'data': description,
                    'color': color,
                    'alignment': alignment,
                    'style': style
                }
            )
        self.data.append(
            {
                'type': 'divider',
                'color': self.BORDER_COLOR,
            }
        )
        self.data.append(
            {
                'gap': '-',
                'type': 'divider',
                'color': self.BORDER_COLOR,
            }
        )

        self._on_update()


    def _on_update(self) -> None:
        self.terminal_size = shutil.get_terminal_size()
        self.terminal_width: int = self.terminal_size.columns
        self.terminal_height: int = self.terminal_size.lines

        self.width = self.terminal_width - 48

        clear()

        for line in self.data:
            color = line.get('color', '')

            if line.get('type', None) == 'divider':
                data: str | list[str] = f'{self.BORDER_COLOR}{'+' if line.get('gap', ' ') == '-' else '|'}{line.get('gap', ' ')}{color}{line.get('style', '')}{line.get('gap', ' ')*self.width}{self.BORDER_COLOR}{line.get('gap', ' ')}{'+' if line.get('gap', ' ') == '-' else '|'}{self.DEFAULT}'
            else:
                text = line['data']
                if len(text) > self.width:
                    text = self._wrapped_text(text)
                
                if isinstance(text, list):
                    data = [
                        f'{self.BORDER_COLOR}|{line.get('gap', ' ')}{color}{line.get('style', '')}{item:{line.get('alignment', Alignment.LEFT)}{self.width}}{self.BORDER_COLOR}{line.get('gap', ' ')}|{self.DEFAULT}'
                        for item in text
                    ]

                else:
                    data = f'{self.BORDER_COLOR}|{line.get('gap', ' ')}{color}{line.get('style', '')}{line['data']:{line.get('alignment', Alignment.LEFT)}{self.width}}{self.BORDER_COLOR}{line.get('gap', ' ')}|{self.DEFAULT}'
            
            if isinstance(data, list):
                for line in data:
                    print(f'{' '*(int((self.terminal_width-self.width)/2))}{line}')
            else:
                print(f'{' '*(int((self.terminal_width-self.width)/2))}{data}')
    

    def _wrapped_text(self, data: str) -> list[str]:
        words = data.split()
        current_line = words[0]

        result = []
        for word in words[1:]:
            if len(current_line) + len(f' {word}') < self.width:
                current_line += f' {word}'
            else:
                result.append(current_line)
                current_line = word
        result.append(current_line)
        return result
    

    def add_line(
            self,
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
            alignment: Literal[
                Alignment.LEFT,
                Alignment.RIGHT,
                Alignment.CENTER
            ] = Alignment.LEFT,
            is_divider: bool = False
        ) -> None:

        if color != '':
            color = foreground(color)
        else:
            color = self.DEFAULT

        if is_divider == True:
            self.data.append(
                {
                    'gap': text,
                    'type': 'divider',
                    'color': self.BORDER_COLOR,
                }
            )
        
        else:
            self.data.append(
                {
                    'data': text,
                    'color': color,
                    'alignment': alignment,
                    'style': style
                }
            )

        self._on_update()


    def add_divider(self) -> None:
        self.data.append(
            {
                'gap': '-',
                'type': 'divider',
                'color': self.BORDER_COLOR,
            }
        )
        self._on_update()
    

    def remove_last(self, count: int = 1) -> None:
        for i in range(count):
            self.data.pop()
        self._on_update()


    def get_input(self,  # This looks so goofy
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

        line: str = f'{' '*indent}{text_color}{text_style}{text}{self.DEFAULT}{input_color}{input_style}'
        response = input(f'{' '*(int(((self.terminal_width-self.width)/2)+2))}{line}')
        
        print(self.DEFAULT, end='')
        
        return response