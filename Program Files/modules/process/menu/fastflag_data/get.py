import json
import os
from typing import Any

from modules.other.paths import FilePath, Directory


def get(profile: str) -> dict:
    default: dict = {
        "name": profile,
        "description": None,
        "enabled": False,
        "data": {}
    }

    path: str = FilePath.FASTFLAGS
    with open(path, 'r') as file:
        fastflag_profiles: list[dict] = json.load(file)
        file.close()
    
    for data in fastflag_profiles:
        if data.get('name', None) == profile:
            return data

    return default


def get_all() -> list[dict]:
    path: str = FilePath.FASTFLAGS
    with open(path, 'r') as file:
        fastflag_profiles: list[dict] = json.load(file)
        file.close()

    return fastflag_profiles