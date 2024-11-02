import platform
import os
import sys
import threading
import json
import webbrowser

from modules.logger import logger
from modules.filesystem import Directory, FilePath, logged_path
from modules.functions.restore_from_mei import restore_from_mei
from modules.info import ProjectData, Hyperlink
from modules import request
from modules.functions.config import settings

from tkinter import messagebox


IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    import pyi_splash


PLATFORM: str = platform.system()


class PlatformError(Exception):
    pass


def run() -> None:
    if not os.path.exists(FilePath.skip_platform_check()):
        if IS_FROZEN:
            pyi_splash.update_text("Checking platform...")
        if PLATFORM != "Windows":
            error_text: str = f"Unsupported OS \"{PLATFORM}\""
            if IS_FROZEN:
                if pyi_splash.is_alive():
                    pyi_splash.close()
            logger.error(error_text)
            raise PlatformError(error_text)
    
    if IS_FROZEN:
        pyi_splash.update_text("Checking core files...")
    check_core_files()
    
    if settings.value("check_for_updates") == True:
        if IS_FROZEN:
            pyi_splash.update_text("Checking for updates...")
        threading.Thread(
            name="startup.check_for_updates()_thread",
            target=check_for_updates,
            daemon=True
        ).start()

    if IS_FROZEN:
        pyi_splash.update_text("Done!")


def check_core_files() -> None:
    logger.info("Checking core files...")
    core_files: list[str] = FilePath.core_files()
    for file in core_files:
        file_exists: bool = os.path.isfile(file)

        if not IS_FROZEN and not file_exists:
            raise FileNotFoundError(logged_path.get(file))

        if IS_FROZEN:
            if file_exists:
                check_file_content(file)
            else:
                restore_from_mei(file)
    
    os.makedirs(Directory.downloaded_mods(), exist_ok=True)
    os.makedirs(Directory.updated_mods(), exist_ok=True)


def check_file_content(file: str) -> None:
    if not IS_FROZEN:
        return

    root: str = Directory.root()
    MEIPASS: str = Directory._MEI()
    path_extension: str = os.path.relpath(file, root)

    if not os.path.isfile(file):
        restore_from_mei(file)

    try:
        with open(file, "r") as current_file:
            current_data: dict = json.load(current_file)
        
        original_filepath: str = os.path.join(MEIPASS, path_extension)
        with open(original_filepath, "r") as original_file:
            original_data: dict = json.load(original_file)
        
        if current_data.keys() == original_data.keys():
            return
        
        filtered_data: dict = original_data.copy()
        for key in filtered_data:
            if key in current_data:
                filtered_data[key] = current_data[key]

        if filtered_data != current_data:
            with open(file, "w") as current_file:
                json.dump(filtered_data, current_file, indent=4)

    except Exception as e:
        logger.warning(f"Failed to verify content of {logged_path.get(file)}, reason: {type(e).__name__}: {e}")


def check_for_updates() -> None:
    logger.info("Checking for updates...")
    
    response: request.Response = request.get(request.GitHubApi.latest_version(), attempts=1)
    data: dict = response.json()
    latest_version: str | None = data.get("latest")
    if latest_version is None:
        return
    
    if latest_version > ProjectData.VERSION:
        logger.debug(f"A newer version is available: {latest_version}")
        if messagebox.askyesno(ProjectData.NAME, f"A newer version is available! Do you wish to update?"):
            webbrowser.open_new_tab(Hyperlink.LATEST_RELEASE)
            logger.info("User chose to update! Shutting down...")
            os._exit(0)