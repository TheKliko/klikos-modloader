"""# launcher.py

launcher.py is a module used in Kliko's modloader,
it's purpose is to take care of the everything that happens when the program is launched with the "-launcher" argument.
"""


import logging
import os
import shutil
import subprocess
import threading
import time

from modules.utils import interface
from modules.utils import read_json
from modules.utils import variables
from modules.utils import write_json

from modules.roblox.updater_studio import check_for_updates


def start() -> None:
    """Function called to begin the launcher process"""

    variables.set(name='rpc_state', value='studio')
    variables.set(name='rpc_timestamp', value=int(time.time()))

    interface.open('Launcher (Studio)')

    interface.text('Checking for updates...')
    check_for_updates()

    apply_mods()
    apply_fastflags()

    thread = threading.Thread(target=launch_roblox_studio, daemon=True)
    thread.start()
    interface.text('Launching Roblox Studio...', spacing=2)
    interface.text('This program will now minimize itself and terminate once Roblox Studio closes', spacing=0)
    time.sleep(5)
    interface.minimize()

    thread.join()  # Wait for Roblox Studio to close


def apply_mods() -> None:
    logging.info('Applying mods...')
    SELECTED_PROFILE: str = variables.get('selected_mod_profile')

    if not SELECTED_PROFILE:
        logging.info('No mod profile selected.')
        return None

    MOD_DIRECTORY: str = variables.get('mod_directory')
    VERSION_DIRECTORY: str = variables.get('version_directory')
    LATEST_VERSION: str = variables.get('latest_studio_version')
    TARGET_DIRECTORY: str = os.path.join(VERSION_DIRECTORY, LATEST_VERSION)

    MOD_PROFILES_FILEPATH: str = variables.get('mod_profiles_filepath')
    MODS: dict = read_json.value(filepath=MOD_PROFILES_FILEPATH, key=SELECTED_PROFILE)

    interface.text(f'Applying mod profile: {SELECTED_PROFILE}')

    for priority, mod in sorted(MODS.items(), key=lambda x: int(x[0]), reverse=True):
        logging.info(f'Applying mod: {mod}')
        interface.text(f'\u2022 Applying mod: {mod}', spacing=0)
        source = os.path.join(MOD_DIRECTORY, mod)
        try:
            shutil.copytree(src=source, dst=TARGET_DIRECTORY, dirs_exist_ok=True)
        except FileNotFoundError as e:
            logging.warning(f'Mod not found: {mod}')
            interface.text(f'    {type(e).__name__}', spacing=0)
        except Exception as e:
            print(type(e).__name__)
            logging.warning(f'Failed to apply mod: {mod}')
            logging.debug(f'{type(e).__name__}')
            interface.text(f'    Failed to apply!', spacing=0)

    logging.info('mods applied!')


def apply_fastflags() -> None:
    logging.info('Applying FastFlags...')
    SELECTED_PROFILE: str = variables.get('selected_fastflag_profile')

    if not SELECTED_PROFILE:
        logging.info('No FastFlag profile selected.')
        return None

    VERSION_DIRECTORY: str = variables.get('version_directory')
    LATEST_VERSION: str = variables.get('latest_studio_version')
    CLIENTSETTINGS_FILEPATH: str = os.path.join(VERSION_DIRECTORY, LATEST_VERSION, 'ClientSettings', 'ClientAppSettings.json')

    FASTFLAG_PROFILES_FILEPATH: str = variables.get('fastflag_profiles_filepath')
    FASTFLAGS: dict = read_json.value(filepath=FASTFLAG_PROFILES_FILEPATH, key=SELECTED_PROFILE)

    interface.text(f'Applying FastFlag profile: {SELECTED_PROFILE}')
    write_json.complete(filepath=CLIENTSETTINGS_FILEPATH, config=FASTFLAGS)

    logging.info('FastFlags applied!')


def launch_roblox_studio() -> None:
    logging.info('Launching Roblox Studio...')
    ROOT_DIRECTORY: str = variables.get('root_directory')
    VERSION_DIRECTORY: str = variables.get('version_directory')
    LATEST_VERSION: str = variables.get('latest_studio_version')
    COMMAND: str = f'"{os.path.join(ROOT_DIRECTORY, VERSION_DIRECTORY, LATEST_VERSION, 'RobloxStudioBeta.exe')}"'
    subprocess.run(COMMAND)


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()