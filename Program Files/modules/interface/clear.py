import os
import platform


def clear() -> None:
    os.system('cls' if platform.system() == 'Windows' else 'clear')