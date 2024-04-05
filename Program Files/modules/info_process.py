import os
import logging
import inspect

from modules.basic_functions import open_console



def info() -> None:
    logging.info(f'Starting {inspect.stack()[0][3]}...')

    open_console()



def main():
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()