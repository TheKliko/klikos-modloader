import logging
import os
import re
import shutil
import threading
from typing import Literal
from tempfile import TemporaryDirectory

from modules import request
from modules.filesystem import Directory, download, extract
from modules.functions import latest_roblox_version, user_channel
from modules.functions import settings

from .filemap import FileMap
from .appsettings import AppSettings


threads: list[threading.Thread] = []


def run(binary_type: Literal["WindowsPlayer","WindowsStudio"], version: str|None = None, channel: str|None = None) -> None:
    def get_manifest(version: str) -> list[str]:
            try:
                url: str = request.RobloxApi.download(version, "rbxPkgManifest.txt")
                response = request.get(url)
                data: str = response.text
                
                manifest: list[str] = re.findall(r'\b\S+\.\S+\b', data)

                # Different options in case I feel like it
                # re.findall(r'\b\S+\.zip\b', data)         # Only get .zip files
                # re.findall(r'\b\S+\.(zip|exe)\b', data)   # Only get .zip or .exe files
                # re.findall(r'\b\S+\.\S+\b', data)         # Get all files

                return manifest

            except Exception as e:
                logging.error(f'[{type(e).__name__}] {str(e)}')
                raise type(e)(str(e))
    
    logging.info("Updating Roblox . . .")
    channel = channel or user_channel.get(binary_type=binary_type)
    version = version or latest_roblox_version.get(binary_type=binary_type, channel=channel)

    version_folder_root: str = os.path.join(Directory.versions(), version)
    if os.path.isdir(version_folder_root):
        shutil.rmtree(version_folder_root, ignore_errors=True)
    os.makedirs(version_folder_root, exist_ok=True)


    use_local_installations: bool = settings.value("use_local_installations", False)
    if use_local_installations == True:
        localappdata: str|None = os.getenv("LOCALAPPDATA")
        if localappdata is not None:
            if os.path.isdir(os.path.join(localappdata, "Roblox", "Versions", version)):
                logging.debug("Updating from local installation")
                shutil.copytree(
                    os.path.join(localappdata, "Roblox", "Versions", version),
                    version_folder_root,
                    dirs_exist_ok=True
                )
                return


    manifest: list[str] = get_manifest(version=version)
    with TemporaryDirectory() as temp_directory:
        for filename in manifest:
            path_extenstion: str|None = FileMap.get_path(filename)
            if path_extenstion:
                target: str = os.path.join(
                    version_folder_root,
                    path_extenstion
                )
            else:
                target = version_folder_root

            thread = threading.Thread(
                name="roblox-installer-thread",
                target=worker,
                kwargs={
                    "temp_directory": temp_directory,
                    "url": request.RobloxApi.download(version=version, file=filename),
                    "filename": filename,
                    "target": target
                },
                daemon=True,
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

    logging.info("Writing AppSettings.xml")
    with open(os.path.join(Directory.versions(), version, "AppSettings.xml"), "w") as file:
        file.write(AppSettings.CONTENT)


def worker(temp_directory, url: str, filename: str, target: str) -> None:
    if not filename.endswith(".zip"):
        download(url=url, destination=os.path.join(target, filename))

    else:
        download(url=url, destination=os.path.join(temp_directory, filename))
        extract(source=os.path.join(temp_directory, filename), destination=target)