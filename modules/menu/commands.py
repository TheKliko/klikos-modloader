import sys
import subprocess
import shutil
from typing import Literal
from pathlib import Path
from tkinter import messagebox, filedialog

from modules import Logger
from modules.info import ProjectData
from modules.filesystem import Directory
from modules import filesystem
from modules.config import mods


IS_FROZEN: bool = getattr(sys, "frozen", False)


# region launch roblox
def launch_roblox_player() -> None:
    if not IS_FROZEN:
        messagebox.showerror(ProjectData.NAME, "Command not available!\nEnvironment not frozen")
        return
    subprocess.Popen([sys.executable, "-l"])


def launch_roblox_studio() -> None:
    if not IS_FROZEN:
        messagebox.showerror(ProjectData.NAME, "Command not available!\nEnvironment not frozen")
        return
    subprocess.Popen([sys.executable, "-s"])
# endregion


# region mods
def add_mods() -> bool:
    initial_dir: Path = Path().home()
    if (initial_dir / "Downloads").is_dir():
        initial_dir = initial_dir / "Downloads"

    files: tuple[str, ...] | Literal[''] = filedialog.askopenfilenames(
        title=f"{ProjectData.NAME} | Import mods", initialdir=initial_dir,
        filetypes=[("ZIP Archives", "*.zip")]
    )

    if files == '':
        return False

    cancelled_imports: int = 0
    for mod in files:
        path: Path = Path(mod)
        name: str = path.with_suffix("").name
        target: Path = Directory.MODS / name

        if target.exists():
            if not messagebox.askokcancel(ProjectData.NAME, "Another mod with the same name already exists!\nDo you wish to replace it?"):
                cancelled_imports += 1
                continue

            try:
                if target.is_file():
                    target.unlink()
                else:
                    shutil.rmtree(target)
            except Exception as e:
                Logger.error(f"Failed to import mod: {name}! {type(e).__name__}: {e}")
                cancelled_imports += 1
                messagebox.showerror(ProjectData.NAME, f"Failed to import mod: {name}!\n{type(e).__name__}: {e}")
                continue


        try:
            filesystem.extract(path, target)
        except Exception as e:
            Logger.error(f"Failed to import mod: {name}! {type(e).__name__}: {e}")
            cancelled_imports += 1
            messagebox.showerror(ProjectData.NAME, f"Failed to import mod: {name}!\n{type(e).__name__}: {e}")
    
    return cancelled_imports < len(files)


def open_mods_folder() -> None:
    filesystem.open(Directory.MODS)


def remove_mod(mod: str) -> None:
    target: Path = Directory.MODS / mod
    try:
        shutil.rmtree(target)
        mods.remove_item(mod)
    except Exception as e:
        Logger.error(f"Failed to remove mod: {mod}! {type(e).__name__}: {e}")
        messagebox.showerror(ProjectData.NAME, f"Something went wrong!\n{type(e).__name__}: {e}")


def rename_mod(mod: str, new: str) -> None:
    target: Path = Directory.MODS / mod

    if target.exists():
        messagebox.showerror(ProjectData.NAME, "Another mod with the same name already exists!")
        return

    try:
        target.rename(target.parent / new)
        mods.set_name(mod, new)
    except Exception as e:
        Logger.error(f"Failed to rename mod: {mod}! {type(e).__name__}: {e}")
        messagebox.showerror(ProjectData.NAME, f"Something went wrong!\n{type(e).__name__}: {e}")
# endregion