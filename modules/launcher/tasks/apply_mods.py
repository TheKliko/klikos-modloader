from pathlib import Path
from typing import Literal
import shutil

from modules import Logger
from modules.filesystem import Directory
from modules.config import mods


def apply_mods(version_folder_root: str | Path, mode: Literal["Player", "Studio"]) -> None:
    version_folder_root = Path(version_folder_root)

    Logger.info("Applying mods...")
    active_mods: list[str] = mods.get_active(mode)
    if not active_mods:
        Logger.info("No active mods!")
        return
    
    for mod in active_mods:
        Logger.info(f"Applying mod: {mod}...")
        mod_folder: Path = Directory.MODS / mod

        try:
            shutil.copytree(mod_folder, version_folder_root, dirs_exist_ok=True)
        
        except Exception as e:
            Logger.error(f"Failed to apply mod: {mod}! {type(e).__name__}: {e}")