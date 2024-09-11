def background(color: str) -> None:
    color = color.removeprefix('#')
    if len(color) == 3:
        color = ''.join([i*2 for i in color])
    if len(color) != 6:
        raise ValueError('Color must be in hexadecimal format (#rrggbb)')

    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)

    print(f'\033]11;rgb:{r:02x}/{g:02x}/{b:02x}\033\\')