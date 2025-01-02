from typing import Literal, Callable
from tkinter import messagebox
from queue import Queue
from pathlib import Path
import time

from modules import Logger
from modules.info import ProjectData
from modules.filesystem import Directory
from modules.config import settings, mods, integrations
from modules.mod_updater import check_for_mod_updates, update_mods
from modules.functions.process_exists import process_exists
from modules.functions.kill_process import kill_process

from ..deployment_info import Deployment
from .check_downloaded_files import check_downloaded_files
from .download_missing_files import download_missing_files
from .restore_default_files import restore_default_files
from .apply_fastflags import apply_fastflags
from .apply_mods import apply_mods
from .launch_roblox import launch_roblox

from customtkinter import StringVar


def run(mode: Literal["Player", "Studio"], textvariable: StringVar, versioninfovariable: StringVar, end_signal: Callable, exception_queue: Queue) -> None:
    try:
        Logger.info("Getting deployment info...")
        deployment: Deployment = Deployment(mode)
        if settings.get_value("show_deployment_info_on_launch"):
            versioninfovariable.set(f"{deployment.version} ({deployment.channel})")

        Logger.info("Checking Downloads folder...")
        missing_file_hashes: list[str] = check_downloaded_files(deployment, mode)

        if missing_file_hashes:
            Logger.info("Downloading missing files...")
            textvariable.set(f"Downloading Roblox {mode}...")
            download_missing_files(deployment, mode, missing_file_hashes)

        if process_exists(deployment.executable_name):
            if not messagebox.askyesno(ProjectData.NAME, "Another Roblox instance is already running!\nDo you still wish to continue?"):
                return
            kill_process(deployment.executable_name)
        
        Logger.info("Restoring default files...")
        textvariable.set(f"Installing Roblox {mode}...")
        restore_default_files(deployment, mode)

        active_mods: list[str] = mods.get_active()
        if integrations.get_value("mod_updater"):
            check: dict[str, list[Path]] | Literal[False] = check_for_mod_updates(Directory.MODS, active_mods, deployment.version)
            if check:
                Logger.info("Updating mods...")
                textvariable.set("Updating mods...")
                update_mods(check, deployment.version, Directory.MODS)

        disable_all_mods: bool = settings.get_value("disable_all_mods")
        disable_all_fastflags: bool = settings.get_value("disable_all_fastflags")
        if not disable_all_mods or not disable_all_fastflags:
            Logger.info("Applying modifications...")
            textvariable.set("Applying modifications...")
        if not disable_all_mods:
            apply_mods(deployment.base_directory, mode)
        if not disable_all_fastflags:
            apply_fastflags(deployment.base_directory, mode)

        Logger.info(f"Launching Roblox {mode}...")
        textvariable.set(f"Launching Roblox {mode}...")
        launch_roblox(str(deployment.executable_path.resolve()))
        time.sleep(2)
    
    except Exception as e:
        exception_queue.put(e)
    
    finally:
        end_signal()