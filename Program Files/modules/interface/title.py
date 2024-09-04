from os import system


def title(title: str = "py.exe") -> None:
    system(f'title {title}')