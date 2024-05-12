"""# updater.py

updater.py is a module used in Kliko's modloader,
it's purpose is to check for updates to the main program.
"""


import logging
import os

from modules.utils import variables
from modules.utils.request_handler import request


class UnknownVersionError(Exception):
    """Exception raised when the current version could not be found"""
    pass


class UpdateAvailableError(Exception):
    """Exception raised when a newer version is available"""
    pass


class LatestVersionNotFoundError(Exception):
    """Exception raised when the latest version could not be found"""
    pass


class DataTransferSuccess(Exception):
    """Exception raised when old data has successfully been transfered, used in startup.py to restart the startup process"""
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
        raise LatestVersionNotFoundError('Failed to get the latest version')
    
    if CURRENT_VERSION != LATEST_VERSION:
        raise UpdateAvailableError(f'A newer version is available: version {LATEST_VERSION}')
    
    logging.info('No updates found')


def transfer_data() -> None:  # Specific to transfering data from v1.0.6 to v1.1.0
    logging.info('Transferring data from older versions...')
    print('First launch detected!')
    print('Transferring data...')

    from modules.utils import read_json
    from modules.utils import write_json
    CONFIG_DIRECTORY: str = variables.get('config_directory')
    SETTINGS_FILEPATH = variables.get('settings_filepath')

    # Transferring settings
    OLD_SETTINGS_FILEPATH: str = os.path.join(CONFIG_DIRECTORY, 'config.json')
    if os.path.isfile(OLD_SETTINGS_FILEPATH):
        OLD_SETTINGS: dict = read_json.complete(filepath=OLD_SETTINGS_FILEPATH)
        user_settings: dict = variables.get('user_settings')
        user_settings['max_log_files']['value'] = OLD_SETTINGS['max_log_files']
        user_settings['launch_roblox_after_setup']['value'] = OLD_SETTINGS['launch_roblox_after_setup']
        write_json.value(filepath=SETTINGS_FILEPATH, key='user_settings', value=user_settings)

        user_directories: dict = variables.get('user_directories')
        user_directories['version_directory'] = OLD_SETTINGS['user_directories']['version_directory']
        user_directories['mod_directory'] = OLD_SETTINGS['user_directories']['mods_directory']
        write_json.value(filepath=SETTINGS_FILEPATH, key='user_directories', value=user_directories)

        write_json.value(filepath=SETTINGS_FILEPATH, key='project_name', value=OLD_SETTINGS['title'])
        write_json.value(filepath=SETTINGS_FILEPATH, key='project_description', value=OLD_SETTINGS['description'])
        write_json.value(filepath=SETTINGS_FILEPATH, key='project_author', value=OLD_SETTINGS['author'])
        write_json.value(filepath=SETTINGS_FILEPATH, key='selected_mod_profile', value=OLD_SETTINGS['selected_mod_profile'])
        write_json.value(filepath=SETTINGS_FILEPATH, key='selected_fastflag_profile', value=OLD_SETTINGS['selected_fastflag_profile'])
        write_json.value(filepath=SETTINGS_FILEPATH, key='installed_roblox_version', value=OLD_SETTINGS['installed_roblox_version'])

    # Transferring mod profiles
    OLD_MOD_PROFILES_FILEPATH = os.path.join(CONFIG_DIRECTORY, 'mod_profiles.json')
    OLD_MOD_PROFILES: dict[str,list] = read_json.complete(filepath=OLD_MOD_PROFILES_FILEPATH)
    if OLD_MOD_PROFILES:
        new_mod_profiles: dict = {}
        for profile, mods in OLD_MOD_PROFILES.items():
            if not isinstance(mods, list):
                new_profile_format = []
                for mod_priority, mod_name in sorted(mods.items()):
                    new_profile_format.append(mod_name)
                new_mod_profiles[profile] = new_profile_format
        if new_mod_profiles:
            write_json.complete(filepath=os.path.join(CONFIG_DIRECTORY, 'mod_profiles.json'), config=new_mod_profiles)

    # Fastflags remain the same, no transfer needed.

    write_json.value(filepath=os.path.join(CONFIG_DIRECTORY, 'version.json'), key='first_launch', value=False)
    raise DataTransferSuccess('Data transferred successfully!')


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()