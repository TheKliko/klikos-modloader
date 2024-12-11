from pathlib import Path
import shutil
import os

from modules import Logger

from .exceptions import ModUpdaterError


def finish_mod_update(mod: str, temporary_directory: Path, output_directory: Path) -> None:
    Logger.info(f"Finishing mod update: {mod}")
    source: Path = temporary_directory / mod
    destination: Path = output_directory / mod

    if not source.is_dir():
        raise ModUpdaterError(f"No such file or directory: %TEMP%/{temporary_directory.name}/{mod}")
    
    destination.mkdir(parents=True, exist_ok=True)
    if not os.access(destination, os.W_OK):
        raise ModUpdaterError(f"Write permission denied for {destination}")

    shutil.rmtree(destination, ignore_errors=True)
    shutil.copytree(source, destination, dirs_exist_ok=True)