from typing import Literal, Callable
from tkinter import messagebox
from queue import Queue
from pathlib import Path
import time
import shutil

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
from .remove_older_versions import remove_older_versions
from .create_singleton_mutex import create_singleton_mutex
from .restore_default_files import restore_default_files
from .apply_fastflags import apply_fastflags
from .apply_mods import apply_mods
from .launch_roblox import launch_roblox
from .start_launch_apps import start_launch_apps

from customtkinter import StringVar


def run(mode: Literal["Player", "Studio"], textvariable: StringVar, versioninfovariable: StringVar, end_signal: Callable, exception_queue: Queue) -> None:
    try:
        # Get deployment info
        Logger.info("Getting deployment info...")
        textvariable.set("Getting deployment info...")
        player_deployment: Deployment = Deployment("Player")
        studio_deployment: Deployment = Deployment("Studio")
        deployment: Deployment = studio_deployment if mode == "Studio" else player_deployment
        if settings.get_value("show_deployment_info_on_launch"):
            versioninfovariable.set(f"{deployment.version} ({deployment.channel})")

        # Forced Roblox reinstallation
        if settings.get_value("force_roblox_reinstallation"):
            Logger.debug("Forced Roblox reinstallation")
            textvariable.set("Forced Roblox reinstallation")
            settings.set_value("force_roblox_reinstallation", False)
            shutil.rmtree(Directory.DOWNLOADS / mode, ignore_errors=True)

        # Check for downloaded files
        Logger.info("Checking Downloads folder...")
        textvariable.set("Checking downloaded files...")
        missing_file_hashes: list[str] = check_downloaded_files(deployment, mode)

        # Download missing files
        if missing_file_hashes:
            Logger.info("Downloading missing files...")
            textvariable.set(f"Downloading Roblox {mode}...")
            download_missing_files(deployment, mode, missing_file_hashes)
        
        # Multi roblox
        multi_roblox: bool = integrations.get_value("multi_roblox")
        if multi_roblox:
            create_singleton_mutex()

        # Check if Roblox is already running
        if not multi_roblox and process_exists(deployment.executable_name):
            if settings.get_value("confirm_launch_if_roblox_running"):
                if not messagebox.askyesno(ProjectData.NAME, "Another Roblox instance is already running!\nDo you still wish to continue?"):
                    return
            kill_process(deployment.executable_name)
        
        disable_all_mods: bool = settings.get_value("disable_all_mods")

        # Remove older Roblox versions
        remove_older_versions(player_deployment.version, studio_deployment.version)

        # Check if current Roblox version is present in the Versions folder
        current_version_installed: bool = False
        if (Directory.VERSIONS / deployment.version / deployment.executable_name).is_file() or (Directory.VERSIONS / deployment.version / "eurotrucks2.exe").is_file():
            current_version_installed = True
        
        # Restore default files, if needed
        if settings.get_value("restore_default_files") or missing_file_hashes or disable_all_mods or not current_version_installed:
            Logger.info("Restoring default files...")
            textvariable.set(f"Installing Roblox {mode}...")
            restore_default_files(deployment, mode)

        # Update mods, if needed
        if integrations.get_value("mod_updater"):
            active_mods: list[str] = mods.get_active(mode)
            check: dict[str, list[Path]] | Literal[False] = check_for_mod_updates(Directory.MODS, active_mods, deployment.version)
            if check:
                Logger.info("Updating mods...")
                textvariable.set("Updating mods...")
                update_mods(check, deployment.version, Directory.MODS)

        # Apply modifications
        disable_all_fastflags: bool = settings.get_value("disable_all_fastflags")
        if not disable_all_mods or not disable_all_fastflags:
            Logger.info("Applying modifications...")
            textvariable.set("Applying modifications...")
        if not disable_all_mods:
            apply_mods(deployment.base_directory, mode)
        if not disable_all_fastflags:
            apply_fastflags(deployment.base_directory, mode)

        # Launch Roblox
        Logger.info(f"Launching Roblox {mode}...")
        textvariable.set(f"Launching Roblox {mode}...")
        launch_roblox(str(deployment.executable_path.resolve()))

        # Start launch apps
        Logger.info("Starting launch apps...")
        start_launch_apps(mode)

        # It takes a second or two for Roblox to appear after it's launched
        time.sleep(2)
    
    except Exception as e:
        exception_queue.put(e)
    
    finally:
        end_signal()