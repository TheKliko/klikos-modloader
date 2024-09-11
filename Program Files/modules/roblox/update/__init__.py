import logging
import os

from modules.other.api import RobloxApi
from modules.other.paths import Directory
from modules.utils import filesystem
from modules.utils import variables

from . import version
from . import filemap
from .app_settings import APP_SETTINGS
from .exceptions import *


def check(binary_type: str, channel: str) -> tuple[bool,str]:
    logging.info('Checking for Roblox updates . . .')
    latest_version: str = version.latest(binary_type, channel)
    return (not version.is_installed(latest_version), latest_version)


def install(binary_type: str, channel: str, latest_version: str) -> None:
    logging.info('Installing Roblox update . . .')

    try:
        roblox_local_reinstall: bool = variables.get('roblox_local_reinstall', {}).get('value', False)
        if roblox_local_reinstall == True:
            is_availabe: bool = version.is_installed_localappdata(latest_version)
            if is_availabe:
                logging.info('Copying local installation from %localappdata%\\Roblox\\Versions')
                source: str = os.path.join(Directory.ROBLOX_LOCALAPPDATA, 'Versions', latest_version)
                target: str = os.path.join(Directory.VERSIONS, latest_version)
                filesystem.copy(source, target)
                return
        
        version_root_directory: str = os.path.join(Directory.VERSIONS, latest_version)

        manifest: list[str] = version.get_manifest(latest_version)
        for filename in manifest:
            path_extension: str | None = filemap.COMMON.get(filename, None)
            if path_extension == None and binary_type == 'WindowsPlayer':
                path_extension: str | None = filemap.ROBLOX_PLAYER.get(filename, None)
            if path_extension == None and binary_type == 'WindowsStudio':
                path_extension: str | None = filemap.ROBLOX_STUDIO.get(filename, None)
            
            if path_extension == None:
                target: str = version_root_directory
            else:
                target: str = os.path.join(version_root_directory, path_extension)

            filesystem.download(RobloxApi.file_download(latest_version, filename), os.path.join(target, filename))

            if filename.endswith('.zip'):
                filesystem.extract(os.path.join(target, filename), target)
                filesystem.remove(os.path.join(target, filename))
        
        logging.info('Writing AppSettings.xml')
        with open(os.path.join(version_root_directory, 'AppSettings.xml'), 'w') as file:
            file.write(APP_SETTINGS)
            file.close()

        logging.info(f'Successfully installed {binary_type} {latest_version}!')

    except Exception as e:
        logging.error(f'[{type(e).__name__}] {str(e)}')
        raise RobloxUpdateError(f'[{type(e).__name__}] {str(e)}')