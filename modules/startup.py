import platform
import os
import sys
import threading
import json
import shutil

from modules.logger import logger
from modules.filesystem import Directory, FilePath, logged_path

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
    
    if IS_FROZEN:
        pyi_splash.update_text("Checking core files...")
    thread = threading.Thread(
        name="startup.check_core_files()_thread",
        target=check_core_files,
        daemon=True
    )
    threads.append(thread)
    thread.start()
    
    if IS_FROZEN:
        pyi_splash.update_text("Checking for updates...")
    update_checker_thread = threading.Thread(
        name="startup.check_for_updates()_thread",
        target=check_for_updates,
        daemon=True
    )
    update_checker_thread.start()
    
    if IS_FROZEN:
        pyi_splash.update_text("Setting registry keys...")
    thread = threading.Thread(
        name="startup.set_registry_keys()_thread",
        target=set_registry_keys,
        daemon=True
    )
    threads.append(thread)
    thread.start()

    for thread in threads:
        thread.join()

    if IS_FROZEN:
        pyi_splash.update_text("Done!")


def check_core_files() -> None:
    logger.info("Checking core files...")
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

    try:
        os.makedirs(os.path.dirname(file), exist_ok=True)
        shutil.copy(os.path.join(MEIPASS, path_extension), os.path.join(root, path_extension))
    except Exception as e:
        logger.error(f"Failed to restore file: {logged_path.get(file)}, reason: {type(e).__name__}: {e}")
    
    # with open(os.path.join(MEIPASS, path_extension), "r") as file1:
    #     data = json.load(file1)

    # os.makedirs(os.path.dirname(file), exist_ok=True)
    # with open(file, "w") as file2:
    #     json.dump(data, file2, indent=4)
    
    logger.warning(f"File restored from _MEI: {logged_path.get(file)}")


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


def check_for_updates() -> None:
    logger.info("Checking for updates...")
    pass


def set_registry_keys() -> None:
    logger.info("Setting registry keys...")
    pass