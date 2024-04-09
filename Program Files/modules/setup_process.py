import os
import logging

def start() -> None:
    logging.info(f'Starting {os.path.splitext(os.path.basename(__file__))[0]}')



def main():
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()