import os
import shutil

from modules.filesystem import Directory


def apply_mods(mods: list[str], version: str) -> None:
    target: str = os.path.join(Directory.versions(), version)
    for mod in mods:
        source: str = os.path.join(Directory.mods(), mod)
        shutil.copytree(source, target, dirs_exist_ok=True)
