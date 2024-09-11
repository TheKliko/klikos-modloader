import sys


def foreground(color: str) -> str:
    color = color.removeprefix('#').lower()
    if len(color) == 3:
        color = ''.join([i*2 for i in color])
    if len(color) != 6:
        raise ValueError('Color must be in hexadecimal format (#rrggbb)')

    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)

    return f'\033[38;2;{r};{g};{b}m'
    # sys.stdout.write(f'\033[38;2;{r};{g};{b}m')
    # sys.stdout.flush()