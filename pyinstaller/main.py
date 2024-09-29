from os import path, name, system
from subprocess import run
from sys import executable, argv, exit


COLOR_RESET: str = "\033[0m"
COLOR_ERROR: str = "\033[38;2;255;107;104m"
COLOR_WARNING: str = "\033[38;2;241;176;12m"
COLOR_URL: str = "\033[38;2;0;168;252m"+'\033[4m'


def main():
    try:
        filepath = path.join(path.dirname(executable), 'Program Files', 'main.py')

        command = ["python", filepath] + argv[1:]
        returncode = run(command).returncode

        if returncode == 9009:
            python_not_found()


    except Exception as e:
        system('cls' if name == 'nt' else 'clear')
        print(COLOR_ERROR+"ERROR: "+type(e).__name__)
        print(COLOR_WARNING+str(e))
        print(COLOR_RESET)
        input("Press ENTER to exit . . .")


def python_not_found() -> None:
    system('cls' if name == 'nt' else 'clear')
    print(COLOR_ERROR+"ERROR: Python was not found!")
    print(COLOR_WARNING+"Please reinstall Python, make sure to check the box that says: \"Add python.exe to PATH\"")
    print(COLOR_RESET)
    print("Python can be downloaded from the Microsoft Store or "+COLOR_URL+"https://www.python.org/downloads/")
    print(COLOR_RESET)
    input("Press ENTER to exit . . .")


if __name__ == "__main__":
    main()