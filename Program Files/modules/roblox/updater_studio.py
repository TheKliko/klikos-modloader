"""# updater.py

updater.py is a module used in Kliko's modloader,
it's purpose is to take care of Roblox updates.
"""


import json
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


class StudioOutdatedError(Exception):
    """Exception raised when the user refused to update Roblox Studio"""
    pass


def check_for_updates() -> None:
    """Function called to check for Roblox Studio updates"""
    logging.info('Checking for Roblox Studio updates...')

    INSTALLED_VERSION: str = variables.get('installed_studio_version')
    LATEST_VERSION: str = latest_studio_version()
    ROOT_DIRECTORY: str = variables.get('root_directory')
    VERSION_DIRECTORY: str = variables.get('version_directory')

    if variables.get('roblox_reinstall_after_changes') and variables.get('mod_profile_changed'):
        update()

    elif INSTALLED_VERSION != LATEST_VERSION or not os.path.isdir(os.path.join(ROOT_DIRECTORY, VERSION_DIRECTORY, LATEST_VERSION)):
        logging.info(f'Studio update available: {LATEST_VERSION}')
        if not variables.get('auto_install_roblox_updates'):
            interface.text(f'A new Roblox Studio version is available: {LATEST_VERSION}', spacing=0)

            if interface.confirm('Do you wish to install this version?'):
                update()
            else:
                logging.debug('Update declined!')
                raise StudioOutdatedError('Update declined!')
        
        else:
            update()
    
    else:
        logging.info('No updates found!')
        interface.text('No updates found!', spacing=0)


def latest_studio_version() -> str:
    # I tried using a 'cleaner' method using this api: https://clientsettingscdn.roblox.com/v2/client-version/windowsstudio, but it seems to return an older version :(
    # DEPLOY_HISTORY_URL: str = r'https://clientsettingscdn.roblox.com/v2/client-version/windowsstudio'
    # VERSION: str = request(url=DEPLOY_HISTORY_URL, request_type='json_value', json_key='clientVersionUpload')
    # variables.set(name='latest_studio_version', value=VERSION)
    # return VERSION

    DEPLOY_HISTORY_URL: str = r'https://setup.rbxcdn.com/DeployHistory.txt'
    DEPLOY_HISTORY: str = request(url=DEPLOY_HISTORY_URL, request_type='text')
    for deployment in reversed(DEPLOY_HISTORY.splitlines()):
        if  'Studio64' in deployment:
            for item in deployment.split():
                if item.startswith('version-'):
                    VERSION: str = item
                    variables.set(name='latest_studio_version', value=VERSION)
                    return VERSION
    return None


def update() -> None:
    logging.info('Updating Roblox Studio...')
    interface.text('Updating Roblox Studio...')

    SETTINGS_FILEPATH: str = variables.get('settings_filepath')

    thread = threading.Thread(target=stop_roblox_studio_installer, daemon=False)
    thread.start()
    start_roblox_studio_installer()
    thread.join()

    version = variables.get('latest_studio_version')
    try:
        copy_version_directory(version)

    except:
        DEPLOY_HISTORY_URL: str = r'https://setup.rbxcdn.com/DeployHistory.txt'
        DEPLOY_HISTORY: str = request(url=DEPLOY_HISTORY_URL, request_type='text')
        versions: list = []
        for deployment in reversed(DEPLOY_HISTORY.splitlines()):
            if  'Studio64' in deployment:
                for item in deployment.split():
                    if item.startswith('version-'):
                        versions.append(item)
            if len(versions) >= 10:
                break
        for version in versions:
            try:
                copy_version_directory(version)
                write_json.value(filepath=SETTINGS_FILEPATH,key='installed_studio_version',value=version)
                variables.set(name='latest_studio_version', value=version)
                return
            except:
                pass

    write_json.value(filepath=SETTINGS_FILEPATH,key='installed_studio_version',value=version)


def start_roblox_studio_installer() -> None:
    PROGRAM_FILES_DIRECTORY: str = variables.get('program_files_directory')
    COMMAND: str = f'"{os.path.join(PROGRAM_FILES_DIRECTORY, 'RobloxStudioInstaller.exe')}"'
    subprocess.run(COMMAND)


def stop_roblox_studio_installer() -> None:
    while True and not variables.get_silent('exit_installer_loop'):
        if process_exists('RobloxStudioBeta.exe'):
            COMMAND_1: str = r'taskkill /f /im RobloxStudioBeta.exe'
            COMMAND_2: str = r'taskkill /f /im RobloxStudioInstaller.exe'
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