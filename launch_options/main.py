from os import path, name, system
from subprocess import run
from sys import executable, argv, exit


def main():
    try:
        filepath = path.join(path.dirname(executable), 'Program Files', 'main.py')

        command = ["python", filepath] + argv[1:]
        returncode = run(command).returncode

        if returncode == 9009:
            python_not_found()


    except Exception as e:
        print("ERROR: "+type(e).__name__)
        print(str(e))
        print()
        input("Press ENTER to exit . . .")
    

    finally:
        exit()


def python_not_found() -> None:
    system('cls' if name == 'nt' else 'clear')
    print("WARNING: Python was not found!")
    print()
    print("Please (re)install Python, make sure to check the box that says: \"Add python.exe to PATH\"")
    print()
    input("Press ENTER to exit . . .")


if __name__ == "__main__":
    main()