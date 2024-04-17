import os
import logging
import multiprocessing
import subprocess
import json
import shutil
import time

from modules import variables
from modules import user_interface as interface
from modules.roblox_update_handler import check_for_update
from modules.json_handler import get_json_value_from_file, get_json_value_from_input, update_json
from modules.directory_functions import copy_directory, create_directory, remove_directory
from modules import rich_presence

from main import root_directory, config_directory

version_directory = variables.get(name='version_directory')


def start() -> None:
    logging.debug(f'Starting {os.path.splitext(os.path.basename(__file__))[0]}')

    config: dict = variables.get('config_json')
    if config['force_roblox_reinstallation'] == True:
        remove_directory(
            source=version_directory,
            name='Version Folder'
        )
        update_json(
            path=os.path.join(config_directory, 'config.json'),
            key='force_roblox_reinstallation',
            value=False
        )

    interface.clear_console()
    interface.open(section='Launcher')
    check_for_update()

    latest_roblox_version = variables.get(name='latest_roblox_version')
    using_latest_version = variables.get(name='using_latest_version')

    if not using_latest_version:
        return None
    
    interface.clear_console()
    interface.open(section='Launcher')
    
    apply_mods()
    apply_fastflags()

    logging.info(f'Launching Roblox {latest_roblox_version}')
    interface.print_message(message='Launching Roblox...')
    process = multiprocessing.Process(target=launch_roblox, args=(latest_roblox_version,))
    process.start()

    variables.set(name='rich_presence_details', value='Playing Roblox')
    variables.set(name='rich_presence_timestamp', value=int(time.time()))
    rich_presence.start()

    process.join(timeout=1)

    logging.debug(f'Finished {os.path.splitext(os.path.basename(__file__))[0]}')
    return None

def apply_mods() -> None:
    config: dict = variables.get(name='config_json')

    selected_mod_profile: str = get_json_value_from_input(
        config=config,
        key='selected_mod_profile'
    )

    if not selected_mod_profile:
        return None

    logging.info(f'Applying mods profile: {selected_mod_profile}')
    interface.print_message(message=f'Applying mods profile: {selected_mod_profile}')

    user_directories: str = get_json_value_from_input(
        config=config,
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

    mod_profile_priorities = get_json_value_from_file(
        path=os.path.join(config_directory, 'mod_profiles.json'),
        key=selected_mod_profile
    )

    try:
        priority_mods: list[str] = []
        for mod_priority, mod_name in mod_profile_priorities.items():
            priority_mods.insert(0, mod_name)

    except:
        pass

    try:
        for mod in os.listdir(os.path.join(root_directory, mods_directory, selected_mod_profile)):
            if not mod in priority_mods:
                logging.info(f'Appling mod: {mod}')
                interface.print_message(message=f'  -> Applying mod: {mod}', spacing=0)
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

    try:
        for mod in priority_mods:
            logging.info(f'Applying priority mod: {mod}')
            interface.print_message(message=f'  -> Applying mod: {mod}', spacing=0)
            shutil.copytree(
                src=os.path.join(root_directory, mods_directory, profile_directory, mod),
                dst=os.path.join(version_directory, latest_roblox_version),
                dirs_exist_ok=True
                )
    
    except Exception as e:
                    logging.info(f'Failed to apply mod: {mod}')
                    interface.print_message(message=f'       -> Failed to apply mod!', spacing=0)

    logging.debug(f'Finished {os.path.splitext(os.path.basename(__file__))[0]}')
    return None

def apply_fastflags() -> None:
    selected_fastflag_profile: str = get_json_value_from_input(
        config=variables.get('config_json'),
        key='selected_fastflag_profile'
    )

    latest_roblox_version: str = variables.get(name='latest_roblox_version')
    client_settings_directory: str = os.path.join(version_directory, latest_roblox_version, 'ClientSettings')

    if not selected_fastflag_profile:
        if os.path.isdir(os.path.join(version_directory, latest_roblox_version, 'ClientSettings')):
            remove_directory(source=client_settings_directory, name='ClientSettings')
        return None

    logging.info(f'Applying FastFlags profile: {selected_fastflag_profile}')
    interface.print_message(message=f'Applying FastFlags profile: {selected_fastflag_profile}')

    try:
        fastflags = get_json_value_from_file(
            path=os.path.join(config_directory, 'fastflag_profiles.json'),
            key=selected_fastflag_profile
        )
        if not os.path.isdir(os.path.join(version_directory, latest_roblox_version, 'ClientSettings')):
            create_directory(path=os.path.join(version_directory, latest_roblox_version), name='ClientSettings')
        with open(os.path.join(client_settings_directory, 'ClientAppSettings.json'), 'w') as file:
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



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()