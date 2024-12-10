from pathlib import Path
from threading import Thread
from queue import Queue
from tempfile import TemporaryDirectory
import shutil
import json

from modules import Logger
from modules.request import Api
from modules.filesystem import download, extract

from .deploy_history import DeployHistory, get_deploy_history


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
            args=(deploy_history, exception_queue, hash, mods),
            daemon=True
        )
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    if not exception_queue.empty():
        e: Exception = exception_queue.get()
        Logger.error(f"{type(e).__name__}: {e}")
        raise e


def hash_specific_worker_thread(deploy_history: DeployHistory, exception_queue: Queue, hash: str, mods: list[Path]) -> None:
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

            Logger.info("Downloading LuaPackages...")
            download_luapackages(deploy_history.LatestVersion.studio, temporary_directory)
            download_luapackages(mod_version, temporary_directory)

            # locate imagesets
            # locate imagesetdata and extract icon data
            # detect modded icons
                # ignore mod if no modded icons were found
                # Just updating info.json will be enough
            # get icon movement
                # ignore mod if no movement was found
                # Just updating info.json will be enough
            # generate new imagesets
                # use imagesets from mod_version
            # finish mod update

    except Exception as e:
        Logger.error(f"{type(e).__name__}: {e}")
        exception_queue.put(e)


def download_luapackages(version: str, output_directory: str | Path) -> None:
    output_directory = Path(output_directory)
    download(Api.Roblox.Deployment.download(version, "extracontent-luapackages.zip"), output_directory / f"{version}-extracontent-luapackages.zip")
    extract(output_directory / f"{version}-extracontent-luapackages.zip", output_directory / version / "ExtraContent" / "LuaPackages")
    (output_directory / f"{version}-extracontent-luapackages.zip").unlink()