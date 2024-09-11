import json
import os
from typing import Any

from modules.other.paths import FilePath, Directory


def get(mod: str) -> dict:
    default: dict = {
        "name": mod,
        "enabled": False,
        "priority": 0
    }

    path: str = FilePath.MODS
    with open(path, 'r') as file:
        mods: list[dict] = json.load(file)
        file.close()
    
    for data in mods:
        if data.get('name', None) == mod:
            return data

    return default


def get_all() -> list[dict]:
    path: str = FilePath.MODS
    with open(path, 'r') as file:
        mods: list[dict] = json.load(file)
        file.close()
    
    for mod in os.listdir(Directory.MODS):
        if mod not in [data.get('name', None) for data in mods]:
            mods.append({'name': mod, 'enabled': False, 'priority': 0})
        continue

    return mods