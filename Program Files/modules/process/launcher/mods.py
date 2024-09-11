import json
import logging
import os
import shutil
import tempfile
from typing import Any

from modules import mod_updater
from modules.other.api import RobloxApi
from modules.other.paths import FilePath, Directory
from modules.utils import filesystem


def get_active() -> list[str]:
    logging.info(f'Getting active mods . . .')
    with open(FilePath.MODS, 'r') as file:
        data: list[str] = json.load(file)
        file.close()
    
    active_mods: list[dict[str, Any]] = []
    for mod in data:
        if mod.get('enabled', False) == True:
            name: str = mod.get('name', None)
            priority = mod.get('priority', 0)
            if name != None:
                active_mods.append({'name': name, 'priority': priority})
    active_mods.sort(key=lambda mod: mod['priority'])
    return [mod['name'] for mod in active_mods]


def get_outdated_mods(version: str, active_mods: list[str]) -> dict[str, list[str]]:
    logging.info(f'Getting outdated mods . . .')
    mods_directory: str = Directory.MODS

    outdated_mods: dict[str, list[str]] = {}
    for mod in active_mods:
        mod_info_path: str = os.path.join(mods_directory, mod, 'info.json')
        if not os.path.isfile(mod_info_path):
            continue

        with open(mod_info_path, 'r') as file:
            data: dict = json.load(file)
            file.close()
        
        mod_version: str = data.get('clientVersionUpload', None)
        if mod_version == None:
            continue

        elif mod_version == version:
            continue

        if outdated_mods.get(mod_version, None) is None:
            outdated_mods[mod_version] = [mod]
        else:
            outdated_mods[mod_version].append(mod)
    
    return outdated_mods


def apply(mods: list[str], version: str) -> None:
    logging.info('Applying mods . . .')
    mods_directory: str = Directory.MODS
    version_directory: str = os.path.join(Directory.VERSIONS, version)
    filesystem.verify(version_directory)

    for mod in mods:
        mod_path: str = os.path.join(mods_directory, mod)
        if not os.path.isdir(mod_path):
            logging.info(f'Failed to apply mod "{mod}": path does not exist!')
            continue

        shutil.copytree(mod_path, version_directory, dirs_exist_ok=True)


def update(mods: dict[str, list[str]], version: str) -> None:
    logging.info(f'Updating mods . . .')

    deploy_history = mod_updater.DeployHistory()

    git_hash_latest: str = None
    for file in deploy_history.ROBLOX_PLAYER:
        if file['version'] == version:
            git_hash_latest = file['git_hash']
            break
    if git_hash_latest is None:
        logging.error('Mod update failed: git_hash_latest is None')
        return

    version_latest_studio: str = None
    for file in deploy_history.ROBLOX_STUDIO:
        if file['git_hash'] == git_hash_latest:
            version_latest_studio = file['version']
            break
    if version_latest_studio is None:
        logging.error('Mod update failed: version_latest_studio is None')
        return

    mod_versions_to_update: list[dict[str, str]] = []
    for mod_version in mods.keys():
        for file in deploy_history.ALL:
            if file['version'] == mod_version:
                git_hash = file['git_hash']
                if git_hash != git_hash_latest and not file['version'] in mod_versions_to_update:
                    mod_versions_to_update.append({
                        'version': file['version'],
                        'git_hash': git_hash
                    })
        
    if mod_versions_to_update == []:
        logging.debug('Mod update cancelled: All mods are already updated')
        return


    with tempfile.TemporaryDirectory() as temp_directory:
        logging.info('Downloading luapackages . . .')

        download_url: str = RobloxApi.file_download(version, 'extracontent-luapackages.zip')
        filesystem.download(download_url, os.path.join(temp_directory, 'extracontent-luapackages.zip'))
        filesystem.extract(os.path.join(temp_directory, 'extracontent-luapackages.zip'), os.path.join(temp_directory, version, 'ExtraContent', 'LuaPackages'))
        filesystem.remove(os.path.join(temp_directory, 'extracontent-luapackages.zip'))

        download_url: str = RobloxApi.file_download(version_latest_studio, 'extracontent-luapackages.zip')
        filesystem.download(download_url, os.path.join(temp_directory, 'extracontent-luapackages.zip'))
        filesystem.extract(os.path.join(temp_directory, 'extracontent-luapackages.zip'), os.path.join(temp_directory, version_latest_studio, 'ExtraContent', 'LuaPackages'))
        filesystem.remove(os.path.join(temp_directory, 'extracontent-luapackages.zip'))

        for mod_data in mod_versions_to_update:
            mod_version: str = mod_data['version']
            download_url: str = RobloxApi.file_download(mod_version, 'extracontent-luapackages.zip')
            filesystem.download(download_url, os.path.join(temp_directory, 'extracontent-luapackages.zip'))
            filesystem.extract(os.path.join(temp_directory, 'extracontent-luapackages.zip'), os.path.join(temp_directory, mod_version, 'ExtraContent', 'LuaPackages'))
            filesystem.remove(os.path.join(temp_directory, 'extracontent-luapackages.zip'))
        
            version_mod_studio: str = None
            for file in deploy_history.ROBLOX_STUDIO:
                if file['git_hash'] == mod_data['git_hash']:
                    version_mod_studio = file['version']
                    git_hash_mod_studio = file['git_hash']
                    break
            if version_mod_studio is None:
                logging.error('Mod update failed: version_mod_studio is None')
                return

            download_url: str = RobloxApi.file_download(version_mod_studio, 'extracontent-luapackages.zip')
            filesystem.download(download_url, os.path.join(temp_directory, 'extracontent-luapackages.zip'))
            filesystem.extract(os.path.join(temp_directory, 'extracontent-luapackages.zip'), os.path.join(temp_directory, version_mod_studio, 'ExtraContent', 'LuaPackages'))
            filesystem.remove(os.path.join(temp_directory, 'extracontent-luapackages.zip'))


            imagesetdata_filepaths: list[dict[str, str]] = []
            for dirpath, dirnames, filenames in os.walk(temp_directory):
                if 'GetImageSetData.lua' in filenames:
                    relative_path: str = os.path.join(os.path.relpath(os.path.join(dirpath, 'GetImageSetData.lua'), temp_directory))
                    imagesetdata_filepaths.append({
                        'version': relative_path.split(os.sep)[0],
                        'path': os.sep.join(relative_path.split(os.sep)[1:])
                    })

            imageset_paths: list[dict[str, str]] = []
            for dirpath, dirnames, filenames in os.walk(temp_directory):
                if 'img_set_1x_1.png' in filenames:
                    relative_path: str = os.path.dirname(os.path.join(os.path.relpath(os.path.join(dirpath, 'GetImageSetData.lua'), temp_directory)))
                    imageset_paths.append({
                        'version': relative_path.split(os.sep)[0],
                        'path': os.sep.join(relative_path.split(os.sep)[1:])
                    })


            icon_maps: dict[str,dict[str,dict[str,str|int]]] = mod_updater.get_icon_maps(temp_directory, imagesetdata_filepaths)

            mods_for_this_version: list[str] = mods[mod_data['version']]
            modded_icons: dict[str,dict[str,list]] = mod_updater.get_modded_icons(mods_for_this_version, imageset_paths, icon_maps, version_mod_studio, temp_directory)

            mod_updater.generate_imagesets(modded_icons, imageset_paths, icon_maps, version_mod_studio, version_latest_studio, temp_directory)

            mod_updater.update_mods(mods_for_this_version, temp_directory, version)