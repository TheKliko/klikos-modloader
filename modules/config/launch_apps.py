import json
from typing import Literal, Optional
from pathlib import Path
from copy import deepcopy

from modules.filesystem import File


FILEPATH: Path = File.LAUNCH_INTEGRATIONS
TEMPLATE: dict = {"launch_args": None, "enabled": False, "enabled_studio": False}


def get_item(key: str) -> dict:
    data: list[dict] = read_file()
    
    for item in data:
        if item.get("filepath") == key:
            return item

    raise KeyError(f"App not found: {key}")


def get_active(mode: Optional[Literal["Player", "Studio"]] = None) -> list[dict]:
    data: list[dict] = read_file()

    if not data:
        return []
    
    match mode:
        case "Player":
            active_apps: list[dict] = [
                item
                for item in data
                if item.get("enabled", False) is True
                and isinstance(item.get("filepath"), str)
            ]

        case "Studio":
            active_apps = [
                item
                for item in data
                if item.get("enabled_studio", False) is True
                and isinstance(item.get("filepath"), str)
            ]
        
        case _:
            active_apps = [
                item
                for item in data
                if (item.get("enabled", False) is True or item.get("enabled_studio", False) is True)
                and isinstance(item.get("filepath"), str)
            ]

    return active_apps


def add_item(filepath: str | Path) -> None:
    filepath = Path(filepath)
    data: list[dict] = read_file()
    new_item: dict = deepcopy(TEMPLATE)
    # new_item["name"] = filepath.name
    new_item["filepath"] = str(filepath.resolve())

    data.insert(0, new_item)
    
    with open(FILEPATH, "w") as file:
        json.dump(data, file, indent=4)


def remove_item(key: str) -> None:
    data: list[dict] = read_file()
    new_data: list[dict] = [item for item in data if item.get("filepath") != key]
    
    if not new_data:
        if FILEPATH.is_file():
            FILEPATH.unlink()
        return
    with open(FILEPATH, "w") as file:
        json.dump(new_data, file, indent=4)


def set_enabled(key: str, value: bool) -> None:
    data: list[dict] = read_file()
    
    for i, item in enumerate(data):
        if item.get("filepath") == key:
            data[i]["enabled"] = value
            break
    
    else:
        raise KeyError(f"App not found in config file: {key}")
    
    with open(FILEPATH, "w") as file:
        json.dump(data, file, indent=4)


def set_enabled_studio(key: str, value: bool) -> None:
    data: list[dict] = read_file()
    
    for i, item in enumerate(data):
        if item.get("filepath") == key:
            data[i]["enabled_studio"] = value
            break
    
    else:
        raise KeyError(f"App not found in config file: {key}")
    
    with open(FILEPATH, "w") as file:
        json.dump(data, file, indent=4)


def set_args(key: str, value: str | None) -> None:
    data: list[dict] = read_file()
    
    for i, item in enumerate(data):
        if item.get("filepath") == key:
            data[i]["launch_args"] = value
            break

    else:
        raise KeyError(f"App not found in config file: {key}")

    with open(FILEPATH, "w") as file:
        json.dump(data, file, indent=4)


def read_file() -> list[dict]:
    if not FILEPATH.is_file():
        return []
    
    with open(FILEPATH, "r") as file:
        data: list[dict] = json.load(file)
    
    return data