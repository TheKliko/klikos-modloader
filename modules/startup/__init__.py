import sys
from tkinter import messagebox
from platform import system

from modules import Logger
from modules.info import ProjectData
from modules.functions.set_registry_keys import set_registry_keys

from .requirements.libraries import check_required_libraries
from .check_for_updates import check_for_updates


def run() -> None:
    # Only check for libraries if the program is running as a Python file instead of an executable
    if not getattr(sys, "frozen", False):
        Logger.info("Checking required libraries")
        check_required_libraries()

    # Only Windows is supported
    user_platform: str = system()
    if user_platform != "Windows":
        messagebox.showwarning(ProjectData.NAME, f"Unsupported OS: '{user_platform}'\nThis program will not work as expected!")

    Logger.info("Checking required files...")
    from .requirements.files import check_required_files
    check_required_files()

    Logger.info("Checking for updates...")
    check_for_updates()

    set_registry_keys()