import sys
from tkinter import messagebox
from platform import system

from modules import Logger
from modules.info import ProjectData
from modules.config import settings

from .requirements.libraries import check_required_libraries
from .check_for_updates import check_for_updates
from .set_registry_keys import set_registry_keys


def run() -> None:
    # Only check for libraries if the program is running as a Python file instead of an executable
    if not getattr(sys, "frozen", False):
        Logger.info("Checking required libraries", prefix="startup")
        check_required_libraries()

    # Only Windows is supported
    user_platform: str = system()
    if user_platform != "Windows":
        messagebox.showwarning(ProjectData.NAME, f"Unsupported OS: '{user_platform}'\nThis program will not work as expected!")

    Logger.info("Checking required files...", prefix="startup")
    from .requirements.files import check_required_files
    check_required_files()

    if settings.get_value("check_for_updates"):
        Logger.info("Checking for updates...", prefix="startup")
        check_for_updates()

    set_registry_keys()