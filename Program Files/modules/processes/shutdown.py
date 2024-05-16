"""# shutdown.py

shutdown.py is a module used in Kliko's modloader,
it's purpose is to take care of the shutdown process for this program.
"""


import logging
import os
import sys

from modules.presence import presence
from modules.utils import variables


def start() -> None:
    """Function called to begin the shutdown process"""
    logging.info('Begin shutdown process')

    variables.set(name='rpc_state', value='shutdown')

    # Any future shutdown code will go here

    presence.stop()

    logging.info('Terminating...')
    sys.exit()


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()