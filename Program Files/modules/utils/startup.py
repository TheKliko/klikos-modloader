"""# startup.py

startup.py is a module used in Kliko's modloader,
it's purpose is to take care of the startup process for this program.
"""


import glob
import time
import logging
import os

from modules.utils import read_json
from modules.utils import updater
from modules.utils import variables
from modules.utils import write_json
from modules.utils.request_handler import request
from modules.utils.updater import LatestVersionNotFoundError, DataTransferSuccess


class SettingsNotFoundError(Exception):
    """Exception raised when settings could not be found locally and could not be loaded remotely"""
    pass


class VersionInfoNotFoundError(Exception):
    """Exception raised when the config file containing version info could not be found locally"""
    pass


def start() -> None:
    """Function called to begin the startup process"""
    logging.info('Begin startup process')

    set_variables() # Also checks for settings.json and version.json
    if variables.get_silent('first_launch'):
        try:
            updater.transfer_data()
        except DataTransferSuccess:
            return start()
    clear_old_logs()
    check_user_directories()

    # Change terminal title using https://stackoverflow.com/a/10229529
    os.system(f'title {variables.get('project_name')}')

    try:
        updater.check_for_update()

    except LatestVersionNotFoundError as e:
        logging.warning('Failed to get the latest version')

    logging.info('End startup process')


def set_variables() -> None:
    logging.info('Setting variables...')
    SETTINGS_FILEPATH: str = variables.get('settings_filepath')
    settings: dict = read_json.complete(filepath=SETTINGS_FILEPATH)
    if not settings:
        logging.warning('Failed to read settings')
        print('Failed to read settings!')
        settings = load_default_settings()
    variables.set(name='settings', value=settings)
    for name, value in settings.items():
        variables.set(name=name, value=value)
    
    USER_DIRECTORIES: dict = variables.get('user_directories')
    VERSION_DIRECTORY: str = os.path.join(variables.get('root_directory'), USER_DIRECTORIES['version_directory'])
    MOD_DIRECTORY: str = os.path.join(variables.get('root_directory'), USER_DIRECTORIES['mod_directory'])
    variables.set(name='version_directory', value=VERSION_DIRECTORY)
    variables.set(name='mod_directory', value=MOD_DIRECTORY)

    USER_SETTINGS: dict = variables.get('user_settings')
    for name, value in USER_SETTINGS.items():
        variables.set(name=name, value=value['value'])

    USEFUL_LINKS: dict = variables.get('links')
    DISCORD_URL: str = USEFUL_LINKS['Discord server']
    WEBSITE_URL: str = USEFUL_LINKS['Official website']
    GITHUB_URL: str = USEFUL_LINKS['GitHub repository']
    variables.set('discord_url', DISCORD_URL)
    variables.set('website_url', WEBSITE_URL)
    variables.set('github_url', GITHUB_URL)

    CONFIG_DIRECTORY: str = variables.get('config_directory')
    VERSION_INFO_FILEPATH: str = os.path.join(CONFIG_DIRECTORY, 'version.json')
    version_info: dict = read_json.complete(filepath=VERSION_INFO_FILEPATH)
    if not version_info:
        raise VersionInfoNotFoundError(f'Could not find required file: {os.path.basename(VERSION_INFO_FILEPATH)}')
    for name, value in version_info.items():
        variables.set(name=name, value=value)

    variables.set(name='rpc_timestamp', value=int(time.time()))
    variables.set(name='rpc_state', value='startup')

    variables.set(name='selected_item_indicator', value='\t<- [SELECTED]')

    return None


def load_default_settings() -> dict | None:
    print('Restoring default settings...')
    logging.debug('Restoring default settings...')
    SETTINGS_FALLBACK: str = variables.get('settings_fallback')
    default_settings: dict = request(request_type='json', url=SETTINGS_FALLBACK)
    if not default_settings:
        raise SettingsNotFoundError('Failed to load settings.')

    SETTINGS_FILEPATH: str = variables.get('settings_filepath')
    write_json.complete(filepath=SETTINGS_FILEPATH, config=default_settings)

    return default_settings


def clear_old_logs() -> None:
    logging.info('Checking for old log files...')
    LOGGING_DIRECTORY: str = variables.get('logging_directory')
    MAX_LOG_FILES: int = variables.get('max_log_files')

    log_files: list = sorted(glob.glob(os.path.join(LOGGING_DIRECTORY, "*.log")), key=os.path.getctime)
    if len(log_files) > MAX_LOG_FILES:
        for i in range(len(log_files)-MAX_LOG_FILES):
            os.remove(log_files[i])
            logging.info(f'Removed old log: {os.path.basename(log_files[i])}')

    return None


def check_user_directories() -> None:
    logging.info('Checking user directories...')
    VERSION_DIRECTORY: str = variables.get('version_directory')
    VERSION_DIRECTORY_EXISTS: bool = os.path.isdir(VERSION_DIRECTORY)
    MOD_DIRECTORY: str = variables.get('mod_directory')
    MOD_DIRECTORY_EXISTS: bool = os.path.isdir(MOD_DIRECTORY)

    if VERSION_DIRECTORY_EXISTS and MOD_DIRECTORY_EXISTS:
        logging.info('No new directories created')
        return None

    if not VERSION_DIRECTORY_EXISTS:
        os.makedirs(VERSION_DIRECTORY, exist_ok=True)
        logging.info(f'Created version directory: {os.path.basename(VERSION_DIRECTORY)}')
    
    if not MOD_DIRECTORY_EXISTS:
        os.makedirs(MOD_DIRECTORY, exist_ok=True)
        logging.info(f'Created mod directory: {os.path.basename(MOD_DIRECTORY)}')
    
    return None


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()