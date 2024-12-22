import json
from pathlib import Path
from typing import Any

from modules.filesystem import File


FILEPATH: Path = File.MODS


def get_active() -> list[str]:
    data: list[dict] = read_file()

    if not data:
        return []
    
    active_mods: list[str] = [
        item["name"] for item in sorted(data, key=lambda item: item["priority"])
        if item["enabled"] is True
    ]

    return active_mods


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