import logging
import os
import subprocess
import threading
import time

from modules.utils import filesystem
from modules.utils import process
from modules.utils import variables
from modules.utils.request import request


class RobloxVersionError(Exception):
    f"""Exception raised by {os.path.basename(__file__)}"""
    pass


class RobloxUpdateError(Exception):
    f"""Exception raised by {os.path.basename(__file__)}"""
    pass


def latest(mode: str = 'roblox') -> str:
    """Return the version ID of the latest Roblox/Studio version"""

    if mode.lower() == 'roblox':
        try:
            USER_CHANNEL_URL: str = r'https://clientsettings.roblox.com/v2/user-channel?binaryType=WindowsPlayer'
            USER_CHANNEL: str = request(USER_CHANNEL_URL, 'json_value', 'channelName')

            VERSION_URL: str = r'https://clientsettingscdn.roblox.com/v2/client-version/windowsplayer/channel/'+USER_CHANNEL
            VERSION: str = request(VERSION_URL, 'json_value', 'clientVersionUpload')

            return VERSION
        except Exception as e:
            logging.error(f'[{type(e).__name__}] {e}')
            raise RobloxVersionError('Failed to get latest Roblox version')

    elif mode.lower() == 'studio':
        # Outdated, returns older versions :(
        # DEPLOY_HISTORY_URL: str = r'https://clientsettingscdn.roblox.com/v2/client-version/windowsstudio'
        # VERSION: str = request(DEPLOY_HISTORY_URL, 'json_value', 'clientVersionUpload')
        # return VERSION

        DEPLOY_HISTORY_URL: str = r'https://setup.rbxcdn.com/DeployHistory.txt'
        DEPLOY_HISTORY: str = request(url=DEPLOY_HISTORY_URL, request_type='text')
        for deployment in reversed(DEPLOY_HISTORY.splitlines()):
            if  'Studio64' in deployment:
                for item in deployment.split():
                    if item.startswith('version-'):
                        VERSION: str = item
                        return VERSION
        raise RobloxVersionError('Failed to get latest Studio version')
    
    else:
        raise RobloxVersionError('Invalid request')


def update(mode: str = 'roblox', version: str = None) -> None:
    """Install Roblox updates"""

    def install() -> None:
        def exit_installer():  # POV: You just learned about nested functions (lol)
            while True and not variables.get('exit_installer_loop'):
                if process.exists(f'{'RobloxStudio' if mode.lower() == 'studio' else 'RobloxPlayer'}Beta.exe'):
                    COMMAND_1: str = f'taskkill /f /im {'RobloxStudio' if mode.lower() == 'studio' else 'RobloxPlayer'}Beta.exe'
                    COMMAND_2: str = f'taskkill /f /im {'RobloxStudio' if mode.lower() == 'studio' else 'RobloxPlayer'}Installer.exe'
                    subprocess.run(COMMAND_1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.run(COMMAND_2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    break
                else:
                    time.sleep(0.5)

        PROGRAM_FILES: str = variables.get('program_files_directory')
        COMMAND: str = f'"{os.path.join(PROGRAM_FILES, f'{'RobloxStudio' if mode.lower() == 'studio' else 'RobloxPlayer'}Installer.exe')}"'

        thread = threading.Thread(target=exit_installer, daemon=False)
        thread.start()
        subprocess.run(COMMAND)
        thread.join()

    logging.info('Updating Roblox')

    ROBLOX_VERSION_FOLDER: str = os.path.join(os.getenv('LOCALAPPDATA'), 'Roblox', 'Versions')
    TARGET_DIRECTORY: str = variables.get('versions_directory')

    if mode.lower() not in ['roblox', 'studio']:
        raise RobloxVersionError('Invalid request')

    try:
        install()
        filesystem.copy_directory(os.path.join(ROBLOX_VERSION_FOLDER, version), os.path.join(TARGET_DIRECTORY, version))
        variables.set('installed_version', version)
    
    except filesystem.ValidationError as e:
        if mode.lower() == 'studio':
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
                    filesystem.copy_directory(os.path.join(ROBLOX_VERSION_FOLDER, version), os.path.join(TARGET_DIRECTORY, version))
                    variables.set('installed_version', version)
                    return
                except:
                    pass
            raise RobloxUpdateError('Failed to update Roblox Studio')


    except Exception as e:
        logging.error(f'[{type(e).__name__}] {e}')
        raise RobloxUpdateError(f'Failed to update {'Roblox Studio' if mode.lower == 'studio' else 'Roblox'}')


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()