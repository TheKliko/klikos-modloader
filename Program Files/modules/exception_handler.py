import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from modules.interface import Color, clear


def run(exception: Exception) -> None:
    if type(exception) == SystemExit:
        logging.info("No errors! Shutting down . . .")
        return
    
    logging.error(type(exception).__name__+": "+str(exception))
    clear()
    print(Color.ERROR+"ERROR: "+type(exception).__name__+"!")
    print(Color.WARNING+str(exception))
    print(Color.RESET)
    input("Press ENTER to close . . .")


def main() -> None:
    try:
        error: str = sys.argv[1]
        message: str = sys.argv[2]
        clear()
        print(Color.ERROR+"ERROR: "+str(error)+"!")
        print(Color.WARNING+str(message))
        print(Color.RESET)
        input("Press ENTER to close . . .")

    except Exception as e:
        run(e)


if __name__ == "__main__":
    main()