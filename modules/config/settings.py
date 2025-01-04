import sys
import json
from pathlib import Path
from typing import Any

from modules.filesystem import File, restore_from_meipass


FILEPATH: Path = File.SETTINGS
IS_FROZEN: bool = getattr(sys, "frozen", False)


def reset_all() -> None:
    restore_from_meipass(FILEPATH)


def get_value(key: str) -> Any:
    item: dict = get_item(key)
    return item["value"]


def set_value(key: str, value: Any) -> None:
    item: dict = get_item(key)
    item["value"] = value
    data: dict = read_file()
    data[key] = item

    with open(FILEPATH, "w") as file:
        json.dump(data, file, indent=4)


def get_item(key: str) -> dict:
    data: dict = read_file()
    
    try:
        return data[key]

    except KeyError:
        raise KeyError(f"Setting not found: {key}")


def read_file() -> dict:
    if not FILEPATH.is_file():
        if not IS_FROZEN:
            raise FileNotFoundError(f"No such file or directory: {FILEPATH}")
        restore_from_meipass(FILEPATH)
    
    with open(FILEPATH, "r") as file:
        data: dict = json.load(file)
    
    return data