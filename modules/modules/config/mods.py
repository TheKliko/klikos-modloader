import json
from copy import deepcopy
from typing import Literal, Optional
from pathlib import Path

from modules.filesystem import File


FILEPATH: Path = File.MODS
TEMPLATE: dict = {"priority": 0, "enabled": False, "enabled_studio": False}


def get_active(mode: Optional[Literal["Player", "Studio"]] = None) -> list[str]:
    data: list[dict] = read_file()

    if not data:
        return []
    
    if mode == "Player":
        active_mods: list[str] = [
            item.get("name")
            for item in sorted(data, key=lambda item: item.get("priority", 0))
            if item.get("enabled", False) is True
            and isinstance(item.get("name"), str)
        ]

    elif mode == "Studio":
        active_mods = [
            item.get("name")
            for item in sorted(data, key=lambda item: item.get("priority", 0))
            if item.get("enabled_studio", False) is True
            and isinstance(item.get("name"), str)
        ]
    
    else:
        active_mods = [
            item.get("name")
            for item in sorted(data, key=lambda item: item.get("priority", 0))
            if (item.get("enabled", False) is True or item.get("enabled_studio", False) is True)
            and isinstance(item.get("name"), str)
        ]

    return active_mods


def get_item(key: str) -> dict:
    data: list[dict] = read_file()
    
    for item in data:
        if item.get("name") == key:
            return item

    raise KeyError(f"Profile not found: {key}")


def remove_item(key: str) -> None:
    data: list[dict] = read_file()
    new_data: list[dict] = [item for item in remove_default_values(data) if item.get("name") != key]
    
    if not new_data:
        if FILEPATH.is_file():
            FILEPATH.unlink()
        return
    with open(FILEPATH, "w") as file:
        json.dump(new_data, file, indent=4)


def set_name(key: str, value: str) -> None:
    data: list[dict] = read_file()
    
    for i, item in enumerate(data):
        if item.get("name") == key:
            data[i]["name"] = value
            break
    
    else:
        return
    
    new_data: list[dict] = remove_default_values(data)
    
    if not new_data:
        if FILEPATH.is_file():
            FILEPATH.unlink()
        return
    with open(FILEPATH, "w") as file:
        json.dump(new_data, file, indent=4)


def set_priority(key: str, value: int) -> None:
    data: list[dict] = read_file()
    
    for i, item in enumerate(data):
        if item.get("name") == key:
            data[i]["priority"] = value
            break
    
    else:
        new_item = deepcopy(TEMPLATE)
        new_item["name"] = key
        new_item["priority"] = value
        data.append(new_item)
    
    new_data: list[dict] = remove_default_values(data)
    
    if not new_data:
        if FILEPATH.is_file():
            FILEPATH.unlink()
        return
    with open(FILEPATH, "w") as file:
        json.dump(new_data, file, indent=4)


def set_enabled(key: str, value: bool) -> None:
    data: list[dict] = read_file()
    
    for i, item in enumerate(data):
        if item.get("name") == key:
            data[i]["enabled"] = value
            break
    
    else:
        new_item = deepcopy(TEMPLATE)
        new_item["name"] = key
        new_item["enabled"] = value
        data.append(new_item)
    
    new_data: list[dict] = remove_default_values(data)
    
    if not new_data:
        if FILEPATH.is_file():
            FILEPATH.unlink()
        return
    with open(FILEPATH, "w") as file:
        json.dump(new_data, file, indent=4)


def set_enabled_studio(key: str, value: bool) -> None:
    data: list[dict] = read_file()
    
    for i, item in enumerate(data):
        if item.get("name") == key:
            data[i]["enabled_studio"] = value
            break
    
    else:
        new_item = deepcopy(TEMPLATE)
        new_item["name"] = key
        new_item["enabled_studio"] = value
        data.append(new_item)
    
    new_data: list[dict] = remove_default_values(data)
    with open(FILEPATH, "w") as file:
        json.dump(new_data, file, indent=4)


def read_file() -> list[dict]:
    if not FILEPATH.is_file():
        return []
    
    with open(FILEPATH, "r") as file:
        data: list = json.load(file)

    return data


def remove_default_values(data: list[dict]) -> list[dict]:
    new_data: list[dict] = [item for item in data if item.get("enabled", TEMPLATE["enabled"]) != TEMPLATE["enabled"] or item.get("enabled_studio", TEMPLATE["enabled_studio"]) != TEMPLATE["enabled_studio"] or item.get("priority", TEMPLATE["priority"]) != TEMPLATE["priority"]]
    return new_data