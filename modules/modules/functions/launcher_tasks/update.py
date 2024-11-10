import os
import shutil
import re
import threading
import queue
from tempfile import TemporaryDirectory

from modules.logger import logger
from modules import request
from modules.request import RobloxApi, GitHubApi, Response
from modules.filesystem import Directory, download, extract
from modules.functions.config import settings


APPSETTINGS: str = "\n".join([
    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
    "<Settings>",
    "\t<ContentFolder>content</ContentFolder>",
    "\t<BaseUrl>http://www.roblox.com</BaseUrl>",
    "</Settings>"
])


def update(latest_version: str) -> None:
    logger.info(f"Downloading Roblox version: {latest_version}")

    if settings.value("use_local_installations"):
        check: bool = do_local_update(latest_version)
        if check:
            return


    logger.info("Getting filemap...")
    response: Response = request.get(GitHubApi.filemap())
    filemap: dict = response.json()

    common_filemap: dict = filemap.get("common", {})
    player_filemap: dict = filemap.get("player", {})
    studio_filemap: dict = filemap.get("studio", {})

    logger.info("Getting package manifest...")
    manifest: list[str] = get_manifest(latest_version)

    logger.info("Downloading files...")
    threads: list[threading.Thread] = []
    exception_queue: queue.Queue = queue.Queue()
    with TemporaryDirectory() as temp_directory:
        for filename in manifest:
            target_extension: str | None = common_filemap.get(filename) or player_filemap.get(filename) or studio_filemap.get(filename)
            if target_extension:
                target: str = os.path.join(Directory.versions(), latest_version, *target_extension)
            else:
                target = os.path.join(Directory.versions(), latest_version)
            
            thread: threading.Thread = threading.Thread(
                name=f"update-downloader-{latest_version}-{filename}",
                target=worker,
                args=(temp_directory, RobloxApi.download(latest_version, filename), filename, target, exception_queue),
                daemon=True
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    
    if not exception_queue.empty():
        error = exception_queue.get()
        raise error
    
    logger.info("Writing AppSettings.xml")
    with open(os.path.join(Directory.versions(), latest_version, "AppSettings.xml"), "w") as file:
        file.write(APPSETTINGS)


def do_local_update(version: str) -> bool:
    logger.info("Attempting local update...")

    localappdata: str | None = os.getenv("LOCALAPPDATA")
    if localappdata is None:
        logger.info("Local update failed!")
        return False
    
    if not os.path.isdir(os.path.join(localappdata, "Roblox", "Versions", version)):
        logger.info("Local update failed!")
        return False
    
    try:
        shutil.copytree(os.path.join(localappdata, "Roblox", "Versions", version), os.path.join(Directory.versions(), version), dirs_exist_ok=True)
        logger.debug("Updated from local installation")
        return True

    except Exception as e:
        logger.info("Local update failed!")
        return False


def get_manifest(version: str) -> list[str]:
    response: Response = request.get(RobloxApi.download(version, "rbxPkgManifest.txt"))
    data: str = response.text
                
    manifest: list[str] = re.findall(r'\b\S+\.\S+\b', data)

    # Different options in case I feel like it
    # re.findall(r'\b\S+\.zip\b', data)         # Only get .zip files
    # re.findall(r'\b\S+\.(zip|exe)\b', data)   # Only get .zip or .exe files
    # re.findall(r'\b\S+\.\S+\b', data)         # Get all files

    return manifest


def worker(temp_directory: str, url: str, filename: str, target: str, exception_queue: queue.Queue) -> None:
    try:
        if not filename.endswith(".zip"):
            download(url=url, destination=os.path.join(target, filename))

        else:
            download(url=url, destination=os.path.join(temp_directory, filename))
            extract(source=os.path.join(temp_directory, filename), destination=target)
    
    except Exception as e:
        exception_queue.put(e)