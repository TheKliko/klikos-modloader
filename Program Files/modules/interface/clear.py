import os


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')