"""# updater.py

updater.py is a module used in Kliko's modloader,
it's purpose is to take care of Roblox updates.
"""


import logging
import os
import shutil
import subprocess
import threading
import time

from modules.utils import interface
from modules.utils import variables
from modules.utils import write_json

from modules.utils.request_handler import request


ROBLOX_INSTALL_DIRECTORY: str = os.path.join(os.getenv('LOCALAPPDATA'), 'Roblox', 'Versions')


class RobloxOutdatedError(Exception):
    """Exception raised when the user refused to update Roblox"""
    pass


def check_for_updates() -> None:
    """Function called to check for Roblox updates"""
    logging.info('Checking for Roblox updates...')

    INSTALLED_VERSION: str = variables.get('installed_roblox_version')
    LATEST_VERSION: str = latest_roblox_version()
    ROOT_DIRECTORY: str = variables.get('root_directory')
    VERSION_DIRECTORY: str = variables.get('version_directory')

    if INSTALLED_VERSION != LATEST_VERSION or not os.path.isdir(os.path.join(ROOT_DIRECTORY, VERSION_DIRECTORY, LATEST_VERSION)):
        logging.info(f'Roblox update available: {LATEST_VERSION}')
        if not variables.get('auto_install_roblox_updates'):
            if not (variables.get('roblox_reinstall_after_changes') and variables.get('mod_profile_changed')):
                interface.text(f'A new Roblox version is available: {LATEST_VERSION}', spacing=0)

                if interface.confirm('Do you wish to install this version?'):
                    update(LATEST_VERSION)
                else:
                    logging.debug('Update declined!')
                    raise RobloxOutdatedError('Update declined!')
        
        else:
            update(LATEST_VERSION)
    
    else:
        logging.info('No updates found!')
        interface.text('No updates found!', spacing=0)
    
    return None


def latest_roblox_version() -> str:
    USER_CHANNEL_URL: str = r'https://clientsettings.roblox.com/v2/user-channel'
    USER_CHANNEL: str = request(url=USER_CHANNEL_URL, request_type='json_value', json_key='channelName')
    VERSION_URL: str = r'https://clientsettingscdn.roblox.com/v2/client-version/windowsplayer/channel/'+USER_CHANNEL
    VERSION: str = request(url=VERSION_URL, request_type='json_value', json_key='clientVersionUpload')
    variables.set(name='latest_version', value=VERSION)
    return VERSION


def update(version) -> None:
    logging.info('Updating Roblox...')
    interface.text('Updating Roblox...')

    SETTINGS_FILEPATH: str = variables.get('settings_filepath')

    thread = threading.Thread(target=stop_roblox_installer, daemon=False)
    thread.start()
    start_roblox_installer()
    thread.join()

    copy_version_directory(version)

    write_json.value(filepath=SETTINGS_FILEPATH,key='installed_roblox_version',value=version)

    return None


def start_roblox_installer() -> None:
    PROGRAM_FILES_DIRECTORY: str = variables.get('program_files_directory')
    COMMAND: str = f'"{os.path.join(PROGRAM_FILES_DIRECTORY, 'RobloxPlayerInstaller.exe')}"'
    subprocess.run(COMMAND)


def stop_roblox_installer() -> None:
    while True and not variables.get_silent('exit_installer_loop'):
        if process_exists('RobloxPlayerBeta.exe'):
            COMMAND_1: str = r'taskkill /f /im RobloxPlayerBeta.exe'
            COMMAND_2: str = r'taskkill /f /im RobloxPlayerInstaller.exe'
            subprocess.run(COMMAND_1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(COMMAND_2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            break
        time.sleep(0.5)


def process_exists(process_name):  # Check if process exists using https://stackoverflow.com/a/29275361
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())


def copy_version_directory(version) -> None:
    ROOT_DIRECTORY: str = variables.get('root_directory')
    VERSION_DIRECTORY: str = variables.get('version_directory')

    SOURCE: str = os.path.join(ROBLOX_INSTALL_DIRECTORY, version)
    DESTINATION: str = os.path.join(ROOT_DIRECTORY, VERSION_DIRECTORY, version)
    shutil.copytree(src=SOURCE, dst=DESTINATION, dirs_exist_ok=True)


def remove_version_directory() -> None:
    ROOT_DIRECTORY: str = variables.get('root_directory')
    VERSION_DIRECTORY: str = variables.get('version_directory')
    TARGET: str = os.path.join(ROOT_DIRECTORY, VERSION_DIRECTORY)
    shutil.rmtree(TARGET)
    logging.warning(f'Deleted Roblox versions directory!')


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()