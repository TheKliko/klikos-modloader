import os
import sys
import shutil
from pathlib import Path

from modules import Logger

from .directories import Directory
from .exceptions import FileRestoreError


IS_FROZEN: bool = getattr(sys, "frozen", False)
ROOT: Path = Directory.ROOT


def restore_from_meipass(file: str | Path) -> None:
    relative_path: Path = Path(file).relative_to(ROOT)

    Logger.info(f"Restoring file from _MEIPASS: {relative_path}")

    if not IS_FROZEN:
        raise FileRestoreError(f"Environment not frozen; cannot restore file: {relative_path}...")
    if not hasattr(sys, "_MEIPASS") or not sys._MEIPASS:
        raise FileRestoreError(f"_MEIPASS directory does not exist; cannot restore file: {relative_path}")

    MEIPASS: Path = Path(sys._MEIPASS)
    backup: Path = MEIPASS / relative_path
    target: Path = ROOT / relative_path
    temp: Path = target.with_suffix(".tmp")

    if not backup.is_file():
        raise FileRestoreError(f"Backup file not found: {relative_path}")
    if not target.parent.is_dir():
        target.parent.mkdir(parents=True, exist_ok=True)
    if not os.access(target.parent, os.W_OK):
        raise FileRestoreError(f"Write permissions denied for {relative_path.parent}")
    
    os.makedirs(target.parent, exist_ok=True)

    try:
        shutil.copy2(backup, temp)
        if target.is_file():
            target.unlink()
        os.replace(temp, target)
    except Exception as e:
        if temp.is_file():
            temp.unlink()
        raise FileRestoreError(f"{type(e).__name__} when restoring {relative_path}: {e}")