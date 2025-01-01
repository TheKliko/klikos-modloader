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
from .generate_new_imagesets import generate_new_imagesets
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
        thread.start()
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
                with open(temporary_directory / mod.name / "info.json", "r") as file:
                    data: dict = json.load(file)
                data["clientVersionUpload"] = deploy_history.LatestVersion.player
                with open(temporary_directory / mod.name / "info.json", "w") as file:
                    json.dump(data, file, indent=4)

            Logger.info(f"Downloading LuaPackages for {hash}")
            download_luapackages(deploy_history.LatestVersion.studio, temporary_directory)
            download_luapackages(mod_version, temporary_directory)

            Logger.info("Locating ImageSets...")
            mod_imageset_path: Path = locate_imagesets(temporary_directory / mod_version)
            latest_imageset_path: Path = locate_imagesets(temporary_directory / deploy_history.LatestVersion.studio)
            
            Logger.info("Locating ImageSetData...")
            mod_imagesetdata_path: Path = locate_imagesetdata_file(temporary_directory / mod_version)
            latest_imagesetdata_path: Path = locate_imagesetdata_file(temporary_directory / deploy_history.LatestVersion.studio)

            Logger.info("Getting icon map...")
            mod_icon_map: dict[str, dict[str, dict[str, str | int]]] = get_icon_map(temporary_directory / mod_version / mod_imagesetdata_path)
            latest_icon_map: dict[str, dict[str, dict[str, str | int]]] = get_icon_map(temporary_directory / deploy_history.LatestVersion.studio / latest_imagesetdata_path)
            
            for mod in mods:
                try:
                    Logger.info("Detecting modded icons...")
                    modded_icons: dict[str, list[str]] = detect_modded_icons((temporary_directory / mod.name / mod_imageset_path), (temporary_directory / mod_version / mod_imageset_path), mod_icon_map)
                    
                    if modded_icons:
                        Logger.info("Generating ImageSets...")
                        generate_new_imagesets(modded_icons, mod_icon_map, latest_icon_map, mod_imageset_path, latest_imageset_path, deploy_history.LatestVersion.studio, mod.name, temporary_directory)
                    
                    Logger.info(f"Finishing mod update: {mod.name}")
                    finish_mod_update(mod.name, temporary_directory, output_directory)

                except Exception as e:
                    Logger.error(f"Failed to update mod: {mod.name} | {type(e).__name__}: {e}")

    except Exception as e:
        Logger.error(f"{type(e).__name__}: {e}")
        exception_queue.put(e)