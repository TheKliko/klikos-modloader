from pathlib import Path
from threading import Thread
from queue import Queue
from tempfile import TemporaryDirectory
import shutil
import json

from modules import Logger

from .deploy_history import DeployHistory, get_deploy_history
from .download_luapackages import download_luapackages
from .locate_imagesets import locate_imagesets
from .locate_imagesetdata_file import locate_imagesetdata_file
from .get_icon_map import get_icon_map
from .detect_modded_icons import detect_modded_icons
from .finish_mod_update import finish_mod_update


def update_mods(check: dict[str, list[Path]], latest_version: str, output_directory: str | Path) -> None:
    Logger.info("Updating mods...")
    output_directory = Path(output_directory)

    deploy_history: DeployHistory = get_deploy_history(latest_version)

    # Each mod will be updated simultaneously
    threads: list[Thread] = []
    exception_queue: Queue = Queue()
    for hash, mods in check.items():
        thread: Thread = Thread(
            name=f"mod_updater.hash_specific_worker_thread({hash})",
            target=hash_specific_worker_thread,
            args=(deploy_history, exception_queue, hash, mods, output_directory),
            daemon=True
        )
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    if not exception_queue.empty():
        e: Exception = exception_queue.get()
        Logger.error(f"{type(e).__name__}: {e}")
        raise e


def hash_specific_worker_thread(deploy_history: DeployHistory, exception_queue: Queue, hash: str, mods: list[Path], output_directory: Path) -> None:
    if hash == deploy_history.get_hash(deploy_history.LatestVersion.player) or not mods:
        return

    mod_version: str = deploy_history.get_studio_version(hash)

    try:
        with TemporaryDirectory(prefix=f"mod_updater_{hash}_") as tmp:
            temporary_directory: Path = Path(tmp)
            Logger.info("Copying mods to temporary directory...")
            for mod in mods:
                shutil.copytree(mod, temporary_directory / mod.name, dirs_exist_ok=True)

            Logger.info("Updating info.json...")
            for mod in mods:
                with open(temporary_directory / mod.name, "r") as file:
                    data: dict = json.load(file)
                data["clientVersionUpload"] = deploy_history.LatestVersion.player
                with open(temporary_directory / mod.name, "w") as file:
                    json.dump(data, file, indent=4)

            Logger.info(f"Downloading LuaPackages for {hash}")
            download_luapackages(deploy_history.LatestVersion.studio, temporary_directory)
            download_luapackages(mod_version, temporary_directory)

            Logger.info("Locating ImageSets...")
            mod_imageset_path: Path = locate_imagesets(temporary_directory / mod.name)
            latest_imageset_path: Path = locate_imagesets(temporary_directory / deploy_history.LatestVersion.studio)
            
            Logger.info("Locating ImageSets...")
            mod_imagesetdata_path: Path = locate_imagesetdata_file(temporary_directory / mod_version)
            latest_imagesetdata_path: Path = locate_imagesetdata_file(temporary_directory / deploy_history.LatestVersion.studio)

            Logger.info("Getting icon map...")
            mod_icon_map: dict[str, dict[str, dict[str, str | int]]] = get_icon_map(temporary_directory / mod_version / mod_imagesetdata_path)
            latest_icon_map: dict[str, dict[str, dict[str, str | int]]] = get_icon_map(temporary_directory / deploy_history.LatestVersion.studio / latest_imagesetdata_path)
            
            Logger.info("Detecting modded icons...")
            # detect modded icons
                # ignore mod if no modded icons were found
                # finish_mod_update()
            # get icon movement
                # ignore mod if no movement was found
                # finish_mod_update()
            # generate new imagesets
                # use imagesets from mod_version
            # finish mod update

    except Exception as e:
        Logger.error(f"{type(e).__name__}: {e}")
        exception_queue.put(e)