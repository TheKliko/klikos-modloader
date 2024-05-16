"""# updater.py

updater.py is a module used in Kliko's modloader,
it's purpose is to check for updates to the main program.
"""


import logging
import os

from modules.utils import interface
from modules.utils import variables
from modules.utils.request_handler import request


class UnknownVersionError(Exception):
    """Exception raised when the current version could not be found"""
    pass


class UpdateAvailableError(Exception):
    """Exception raised when a newer version is available"""
    pass


def check_for_update() -> None:
    """Function called to check if the program is running on the latest version"""

    logging.info('Checking for updates...')

    CURRENT_VERSION: str = variables.get('version')
    if not CURRENT_VERSION:
        raise UnknownVersionError('Failed to get the current version')

    LATEST_VERSION_URL: str = r'https://raw.githubusercontent.com/TheKliko/roblox-modloader/main/Program%20Files/config/version.json'
    LATEST_VERSION: str = request(url=LATEST_VERSION_URL, request_type='json_value', json_key='version')
    if not LATEST_VERSION:
        print('Failed to find the latest version!')
        logging.warning('Failed to find the latest version!')
        return None

    if CURRENT_VERSION != LATEST_VERSION:
        interface.text(f'A newer version is available: version {LATEST_VERSION}')
        if interface.confirm(prompt='Do you wish to update?'):
            raise UpdateAvailableError(f'A newer version is available: version {LATEST_VERSION}')

    else:
        logging.info('No updates found')


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()