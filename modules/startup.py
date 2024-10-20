import platform
import time
import os
import sys
import threading
import json

from modules.logger import logger
from modules.filesystem import Directory, FilePath
from modules import filesystem

IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    import pyi_splash


PLATFORM: str = platform.system()
threads: list[threading.Thread] = []


class PlatformError(Exception):
    pass


def run() -> None:
    if IS_FROZEN:
        pyi_splash.update_text("Checking platform...")
    if PLATFORM != "Windows":
        raise PlatformError(f"Unsupported OS \"{PLATFORM}\" detected!")
    
    # Move log statements to INSIDE THE FUNCTION BEING CALLED
    logger.info("Checking core files...")
    if IS_FROZEN:
        pyi_splash.update_text("Checking core files...")
    thread = threading.Thread(
        name="startup.check_core_files()_thread",
        target=check_core_files,
        daemon=True
    )
    # time.sleep(1)
    
    logger.info("Checking for updates...")
    if IS_FROZEN:
        pyi_splash.update_text("Checking for updates...")
    # time.sleep(1)
    
    logger.info("Setting registry keys...")
    if IS_FROZEN:
        pyi_splash.update_text("Setting registry keys...")
    # time.sleep(1)
    
    if IS_FROZEN:
        pyi_splash.update_text("Done!")
    # time.sleep(1)

    for thread in threads:
        thread.join()


def check_core_files() -> None:
    core_files: list[str] = FilePath.core_files()
    for file in core_files:
        if os.path.isfile(file):
            if IS_FROZEN:
                check_file_content(file)
            continue

        elif IS_FROZEN:
            restore_core_file(file)
        
        else:
            raise FileNotFoundError(os.path.join(os.path.basename(os.path.dirname(file)), os.path.basename(file)))


def restore_core_file(file: str) -> None:
    if not IS_FROZEN:
        return
    root: str = Directory.root()
    MEIPASS: str = Directory._MEI()
    path_extension: str = os.path.relpath(file, root)

    with open(os.path.join(MEIPASS, path_extension), "r") as file1:
        data = json.load(file1)

    os.makedirs(file, exist_ok=True)
    with open(file, "w") as file2:
        json.dump(data, file2, indent=4)
    
    logger.warning(f"File restored from _MEI: {path_extension}")


def check_file_content(file: str) -> None:
    if not IS_FROZEN:
        return
    root: str = Directory.root()
    MEIPASS: str = Directory._MEI()
    path_extension: str = os.path.relpath(file, root)

    with open(file, "r") as file1:
        current_data: dict = json.load(file1)
    
    test: str = os.path.join(MEIPASS, path_extension)
    with open(test, "r") as file2:
        new_data: dict = json.load(file2)
    
    for key in new_data:
        if key not in current_data:
            restore_core_file(file)