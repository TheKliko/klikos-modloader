import sys
import subprocess
from tkinter import messagebox

from modules.info import ProjectData


IS_FROZEN: bool = getattr(sys, "frozen", False)


def launch_roblox_player() -> None:
    if not IS_FROZEN:
        messagebox.showerror(ProjectData.NAME, "Command unavailable!\nEnvironment not frozen")
        return
    subprocess.Popen([sys.executable, "-l"])


def launch_roblox_studio() -> None:
    if not IS_FROZEN:
        messagebox.showerror(ProjectData.NAME, "Command unavailable!\nEnvironment not frozen")
        return
    subprocess.Popen([sys.executable, "-s"])


def add_mods() -> None:
    pass


def open_mods_folder() -> None:
    pass