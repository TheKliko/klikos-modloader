from pathlib import Path
import shutil
import os

from .exceptions import ModUpdaterError


def finish_mod_update(mod: str, temporary_directory: Path, output_directory: Path) -> None:
    source: Path = temporary_directory / mod
    destination: Path = output_directory / mod

    if not source.is_dir():
        raise ModUpdaterError(f"No such file or directory: %TEMP%/{temporary_directory.name}/{mod}")
    
    destination.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if not os.access(destination, os.W_OK):
            raise ModUpdaterError(f"Write permission denied for {destination}")
        if destination.is_dir():
            shutil.rmtree(destination)
        elif destination.is_file():
            destination.unlink()

    source.rename(destination)
    # shutil.copytree(source, destination, dirs_exist_ok=True)