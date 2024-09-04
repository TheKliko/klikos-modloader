import os

from modules.other.paths import Directory


def is_installed(version) -> bool:
    versions_directory: str = Directory.VERSIONS
    
    path = os.path.join(versions_directory, version)

    return os.path.isdir(path) and (os.path.isfile(os.path.join(path, 'RobloxPlayerBeta.exe')) or os.path.isfile(os.path.join(path, 'RobloxStudioBeta.exe')))


def is_installed_localappdata(version) -> bool:
    versions_directory: str = os.path.join(Directory.ROBLOX_LOCALAPPDATA, 'Versions')
    
    path = os.path.join(versions_directory, version)

    return os.path.isdir(path) and (os.path.isfile(os.path.join(path, 'RobloxPlayerBeta.exe')) or os.path.isfile(os.path.join(path, 'RobloxStudioBeta.exe')))