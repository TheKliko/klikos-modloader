import os
import sys
import webbrowser

from modules import interface
from modules.utils import interface_response_validation as irv
from modules.utils import json_manager
from modules.utils import variables
from modules.utils.request import request, RequestType


class UpdateAvailableError(Exception):
    """Exception raised when an update is available"""
    pass


BULLET: str = '\u2022'


def check() -> None:
    SETTINGS_FILEPATH: str = variables.get('settings_filepath')
    USER_SETTINGS: dict = json_manager.read(SETTINGS_FILEPATH, 'user_settings')
    CHECK_FOR_UPDATES: bool = USER_SETTINGS['check_for_updates']['value']

    if CHECK_FOR_UPDATES == False:
        return
    
    VERSION_INFO: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/version.json'
    LATEST_VERSION: str = request(VERSION_INFO, RequestType.JSON_VALUE, 'latest')

    PROJECT_DATA: dict = variables.get('project_data')
    CURRENT_VERSION: str = variables.get('project_data')['version']

    if CURRENT_VERSION < LATEST_VERSION:
        interface.open(['A newer version is available', f'Version {LATEST_VERSION}'])
        interface.text('Would you like to download this version?')
        interface.divider()
        while True:
            response: str = interface.prompt()
            validation = irv.boolean(response)
            if irv.boolean(response)[0] == True:
                if validation[1] == False:
                    return
                
                webbrowser.open(r'https://github.com/TheKliko/klikos-modloader/releases/latest', 2, True)
                sys.exit()

            else:
                interface.open(['An Update Is Available', LATEST_VERSION])
                interface.text('Would you like to download this version?')
                interface.divider()
                interface.text(
                    [
                        f'Invalid response: \'{response}\'',
                        f'Accepted responses are [Y/N]'
                    ]
                )
                interface.divider()


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()