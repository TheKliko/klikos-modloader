import sys
import subprocess
import shutil
from pathlib import Path
from tkinter import messagebox

from modules.info import ProjectData
from modules.filesystem import Directory
from modules import filesystem


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
    filesystem.open(Directory.MODS)


def remove_mod(mod: str) -> None:
    target: Path = Directory.MODS / mod

    pass