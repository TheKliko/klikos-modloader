import logging
import os
import subprocess
import sys
import threading
import time

from modules import interface
from modules.roblox import version
from modules.utils import filesystem
from modules.utils import json_manager
from modules.utils import process
from modules.utils import registry_editor
from modules.utils import variables
from modules.presence.status import RichPresenceStatus


BULLET: str = '\u2022'


class LauncherError(Exception):
    f"""Exception raised by {os.path.basename(__file__)}"""
    pass


def run(mode: str = 'roblox') -> None:
    """Begin the launcher process"""

    logging.info(f'Launching Roblox with launch-mode: {mode}')
    variables.set('rpc_status', RichPresenceStatus.LAUNCHER)

    LAUNCH_MODE: str = mode
    SETTINGS_FILEPATH: str = variables.get('settings_filepath')
    VERSION_FOLDER: str = variables.get('versions_directory')
    USING_RPC: bool = variables.get('discord_rpc')
    
    launch_configuration: dict = json_manager.read(SETTINGS_FILEPATH, 'launch_configuration')
    FORCE_ROBLOX_REINSTALLATION: bool = launch_configuration['force_roblox_reinstallation']

    if FORCE_ROBLOX_REINSTALLATION == True:
        filesystem.remove_directory([item for item in filesystem.subdirectories(VERSION_FOLDER, True)])
        launch_configuration['force_roblox_reinstallation'] = False
        json_manager.update(SETTINGS_FILEPATH, 'launch_configuration', launch_configuration)

    if not LAUNCH_MODE in ['roblox', 'studio']:
        raise LauncherError('Invalid launch mode')
    
    close_existing_sessions(LAUNCH_MODE)

    interface.open(f'Launching Roblox {'Studio' if LAUNCH_MODE.lower() == 'studio' else 'Player'}')
    interface.text(f'{BULLET} Checking for updates...')
    interface.divider()

    check_for_updates(LAUNCH_MODE)
    registry_editor.set_registry_key()
    LATEST_VERSION: str = variables.get('latest_version')
    INSTALLED_VERSION: str = variables.get('installed_version') or LATEST_VERSION

    if launch_configuration['selected_mod_profile']:
        interface.open(f'Launching Roblox {'Studio' if LAUNCH_MODE.lower() == 'studio' else 'Player'}')
        interface.text(f'{BULLET} Checking for updates...')
        interface.text(f'{BULLET} Applying mods...')
        interface.divider()
        apply_mods(INSTALLED_VERSION)
    
    if launch_configuration['selected_fastflag_profile']:
        interface.open(f'Launching Roblox {'Studio' if LAUNCH_MODE.lower() == 'studio' else 'Player'}')
        interface.text(f'{BULLET} Checking for updates...')
        if launch_configuration['selected_mod_profile']:
            interface.text(f'{BULLET} Applying mods...')
        interface.text(f'{BULLET} Applying FastFlags...')
        interface.divider()
        apply_fastflags(INSTALLED_VERSION, LAUNCH_MODE)

    thread = threading.Thread(target=launch_roblox, args=(LAUNCH_MODE, INSTALLED_VERSION or LATEST_VERSION), daemon=True)
    thread.start()

    interface.open(f'Launching Roblox {'Studio' if LAUNCH_MODE.lower() == 'studio' else 'Player'}')
    interface.text(f'{BULLET} Checking for updates...')
    if launch_configuration['selected_mod_profile']:
        interface.text(f'{BULLET} Applying mods...')
    if launch_configuration['selected_fastflag_profile']:
        interface.text(f'{BULLET} Applying FastFlags...')
    interface.text(f'{BULLET} Launching modded {LAUNCH_MODE.title()}...')
    interface.divider()

    if USING_RPC:
        variables.set('rpc_status', RichPresenceStatus.STUDIO if LAUNCH_MODE == 'studio' else RichPresenceStatus.ROBLOX)
        interface.text('In order to update your Discord RPC status, this program will minimize itself and keep running in the background')
        interface.text('It will automatically terminate when you exit Roblox')
        interface.divider()

        time.sleep(5)
        interface.minimize()
        logging.info('Waiting for Roblox to close')
        thread.join()

    else:
        interface.text('Because you have disabled Discord RPC, this program will now terminate')
        interface.divider()
        time.sleep(5)


def close_existing_sessions(launch_mode) -> None:
    logging.info('Closing existing sessions')
    MODE: str = 'RobloxStudio' if  launch_mode == 'studio' else 'RobloxPlayer'

    try:
        if process.exists(f'{MODE}Installer.exe'):
            process.close(f'{MODE}Installer.exe')

        if process.exists(f'{MODE}Beta.exe'):
            process.close(f'{MODE}Beta.exe')
    
    except Exception as e:
        raise LauncherError(f'Failed to close existing Roblox session: [{type(e).__name__}] {str(e)}')


def check_for_updates(launch_mode: str) -> None:
    logging.info('Checking for updates')
    variables.set('rpc_state', 'Checking for updates...')
    versions_directory: str = variables.get('versions_directory')
    LATEST_VERSION: str = version.latest(launch_mode)
    variables.set('latest_version', LATEST_VERSION)

    if launch_mode == 'roblox':
        if not os.path.isdir(os.path.join(versions_directory, LATEST_VERSION)):
            variables.set('rpc_state', 'Updating Roblox...')
            version.update(launch_mode, LATEST_VERSION)
            variables.remove('rpc_state')

    elif launch_mode == 'studio':
        if not os.path.isdir(os.path.join(versions_directory, LATEST_VERSION)):
            variables.set('rpc_state', 'Updating Roblox Studio...')
            version.update(launch_mode, LATEST_VERSION)
            variables.remove('rpc_state')


def apply_mods(version: str = None) -> None:
    logging.info('Applying mods')
    variables.set('rpc_state', 'Applying mods...')

    try:
        LAUNCH_CONFIGURATION: dict = variables.get('launch_configuration')
        SELECTED_MOD_PROFILE: str = LAUNCH_CONFIGURATION['selected_mod_profile']
        MODS_DIRECTORY: str = variables.get('mods_directory')
        VERSIONS_DIRECTORY: str = variables.get('versions_directory')
        TARGET_DIRECTORY: str = os.path.join(VERSIONS_DIRECTORY, version)

        MOD_PROFILES_FILEPATH: str = variables.get('mod_profiles_filepath')
        MOD_PROFILE_DATA: dict = json_manager.read(MOD_PROFILES_FILEPATH, SELECTED_MOD_PROFILE)

        for priority, mod in sorted(MOD_PROFILE_DATA.items(), key=lambda x: int(x[0]), reverse=True):
            source: str = os.path.join(MODS_DIRECTORY, mod)
            filesystem.copy_directory(source, TARGET_DIRECTORY)
    
    except Exception as e:
        raise LauncherError(f'Failed to apply mods: [{type(e).__name__}] {str(e)}')


def apply_fastflags(version: str = None, launch_mode: str = None) -> None:
    logging.info('Applying FastFlags')
    variables.set('rpc_state', 'Applying FastFlags...')

    try:
        LAUNCH_CONFIGURATION: dict = variables.get('launch_configuration')
        SELECTED_FASTFLAG_PROFILE: str = LAUNCH_CONFIGURATION['selected_fastflag_profile']
        VERSIONS_DIRECTORY: str = variables.get('versions_directory')
        TARGET_DIRECTORY: str = os.path.join(VERSIONS_DIRECTORY, version, 'ClientSettings')
        TARGET_FILE: str = os.path.join(TARGET_DIRECTORY, 'StudioAppSettings.json' if launch_mode.lower() == 'studio' else 'ClientAppSettings.json')
        filesystem.validate(TARGET_DIRECTORY, filesystem.ValidationMode.DIRECTORY)

        FASTFLAG_PROFILES_FILEPATH: str = variables.get('fastflag_profiles_filepath')
        FASTFLAG_PROFILE: dict = json_manager.read(FASTFLAG_PROFILES_FILEPATH, SELECTED_FASTFLAG_PROFILE)

        json_manager.write(TARGET_FILE, FASTFLAG_PROFILE)
    
    except Exception as e:
        raise LauncherError(f'Failed to apply mods: [{type(e).__name__}] {str(e)}')


def launch_roblox(mode: str = 'roblox', version: str = None) -> None:
    logging.debug(f'Launching Roblox {'Studio' if mode.lower() == 'studio' else 'Player'}')
    variables.set('rpc_state', f'Launching Roblox {'Studio' if mode.lower() == 'studio' else 'Player'}...')
    versions_directory: str = variables.get('versions_directory')

    roblox_launch_args: str = variables.get('roblox_launch_args')
    if roblox_launch_args:
        for item in [item for item in roblox_launch_args.split('+') if item.startswith('launchtime:')]:
            new_item: str = f'launchtime:{str(int(time.time() * 1000))}'
            roblox_launch_args.replace(item, new_item)
    COMMAND: str = f'"{os.path.join(versions_directory, version, f'{'RobloxStudio' if mode.lower() == 'studio' else 'RobloxPlayer'}Beta.exe')}" {roblox_launch_args}' if roblox_launch_args else f'"{os.path.join(versions_directory, version, f'{'RobloxStudio' if mode.lower() == 'studio' else 'RobloxPlayer'}Beta.exe')}"'
    subprocess.run(COMMAND)


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()