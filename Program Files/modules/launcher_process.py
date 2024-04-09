import os
import logging
import multiprocessing
import subprocess
import json

from modules import variables
from modules import user_interface as interface
from modules.roblox_update_handler import check_for_update
from modules.json_handler import get_json_value_from_file, get_json_value_from_input
from modules.directory_functions import copy_directory, create_directory

from main import root_directory, config_directory

version_directory = variables.get(name='version_directory')


def start() -> None:
    logging.debug(f'Starting {os.path.splitext(os.path.basename(__file__))[0]}')

    interface.open()
    check_for_update()

    latest_roblox_version = variables.get(name='latest_roblox_version')
    using_latest_version = variables.get(name='using_latest_version')

    if not using_latest_version:
        return None
    
    apply_mods()
    apply_fastflags()

    logging.info(f'Launching Roblox {latest_roblox_version}')
    interface.print_message(message='Launching Roblox...')
    process = multiprocessing.Process(target=launch_roblox, args=(latest_roblox_version,))
    process.start()
    process.join(timeout=5)

    logging.debug(f'Finished {os.path.splitext(os.path.basename(__file__))[0]}')
    return None

def apply_mods() -> None:
    selected_mod_profile: str = get_json_value_from_input(
        config=variables.get('config_json'),
        key='selected_mod_profile'
    )

    if not selected_mod_profile:
        return None

    logging.info(f'Applying mods profile: {selected_mod_profile}')
    interface.print_message(message=f'Applying mods profile: {selected_mod_profile}')

    user_directories: str = get_json_value_from_input(
        config=variables.get('config_json'),
        key='user_directories'
    )
    mods_directory: str = get_json_value_from_input(
        config=user_directories,
        key='mods_directory'
    )
    profile_directory: str = os.path.join(
        root_directory, mods_directory, selected_mod_profile
    )
    latest_roblox_version: str = variables.get(name='latest_roblox_version')

    try:
        for mod in os.listdir(os.path.join(root_directory, mods_directory, selected_mod_profile)):
            logging.info(f'Appling mod: {mod}')
            interface.print_message(message=f'Applying mod: {mod}', spacing=0)
            try:
                copy_directory(
                    source = os.path.join(root_directory, mods_directory, profile_directory, mod),
                    destination = os.path.join(version_directory, latest_roblox_version)
                )

            except Exception as e:
                logging.info(f'Failed to apply mod: {mod}')
                interface.print_message(message=f'Failed to apply mod: {mod}', spacing=0)

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def apply_fastflags() -> None:
    selected_fastflag_profile: str = get_json_value_from_input(
        config=variables.get('config_json'),
        key='selected_fastflag_profile'
    )

    if not selected_fastflag_profile:
        return None

    logging.info(f'Applying fastflags profile: {selected_fastflag_profile}')
    interface.print_message(message=f'Applying fastflags profile: {selected_fastflag_profile}')

    latest_roblox_version: str = variables.get(name='latest_roblox_version')
    client_settings_directory: str = os.path.join(version_directory, latest_roblox_version, 'ClientSettings')

    try:
        fastflags = get_json_value_from_file(
            path=os.path.join(config_directory, 'fastflag_profiles.json'),
            key=selected_fastflag_profile
        )
        if not os.path.isdir(os.path.join(version_directory, latest_roblox_version, 'ClientSettings')):
            create_directory(path=os.path.join(version_directory, latest_roblox_version), name='ClientSettings')
        with open(os.path.join(version_directory, latest_roblox_version, 'ClientSettings', 'ClientAppSettings.json'), 'w') as file:
            file.write(json.dumps(fastflags, indent=4))
            file.close()

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def launch_roblox(latest_roblox_version: str) -> None:
    try:
        command: str = f'{os.path.join(version_directory, latest_roblox_version, 'RobloxPlayerBeta.exe')}'
        subprocess.run(command)

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None



def main():
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()