import sys
from tkinter import messagebox
from platform import system

from modules.info import ProjectData

from .requirements.libraries import check_required_libraries
from .check_for_updates import check_for_updates


def run() -> None:
    # Only check for libraries if the program is running as a Python file instead of an executable
    if not getattr(sys, "frozen", False):
        check_required_libraries()

    # Only Windows is supported
    user_platform: str = system()
    if user_platform != "Windows":
        messagebox.showwarning(ProjectData.NAME, f"Unsupported OS: '{user_platform}'\nThis program will not work as expected!")

    from .requirements.files import check_required_files
    check_required_files()

    check_for_updates()