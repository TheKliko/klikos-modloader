import json
from pathlib import Path
from typing import Any

from modules.filesystem import File


FILEPATH: Path = File.FASTFLAGS


def get_active() -> dict:
    data: list[dict] = read_file()

    if not data:
        return {}
    
    active_fastflags: dict = {}
    for profile in data:
        if profile["enabled"] is True:
            active_fastflags.update(profile["data"])

    return active_fastflags


def get_item(key: str) -> dict:
    data: list[dict] = read_file()
    
    for item in data:
        if item["name"] == key:
            return item

    raise KeyError(f"Profile not found: {key}")


def read_file() -> list[dict]:
    if not FILEPATH.is_file():
        return []
    
    with open(FILEPATH, "r") as file:
        data: list = json.load(file)
    
    return data