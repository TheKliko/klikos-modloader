import json
from pathlib import Path
from typing import Optional, Literal
from copy import deepcopy

from modules.filesystem import File


FILEPATH: Path = File.FASTFLAGS
TEMPLATE: dict = {"description": None, "enabled": False, "enabled_studio": False, "data": {"ExampleFlag": "ExampleValue"}}


def get_active(mode: Optional[Literal["Player", "Studio"]] = None) -> dict:
    data: list[dict] = read_file()

    if not data:
        return {}
    
    active_profiles: list[dict] = [
        item.get("data")
        for item in data
        if isinstance(item.get("data"), dict) and item.get("data", {})
        and (
            item.get("enabled", False) if mode == "Player"
            else item.get("enabled_studio", False) if mode == "Studio"
            else (item.get("enabled", False) or item.get("enabled_studio", False))
        )
    ]
    
    active_fastflags: dict = {}
    for profile in active_profiles:
        active_fastflags.update(profile)

    return active_fastflags


def get_item(key: str) -> dict:
    data: list[dict] = read_file()
    
    for item in data:
        if item["name"] == key:
            return item

    raise KeyError(f"Profile not found: {key}")


def add_item(key: str, description: str | None = None, profile_data: dict = TEMPLATE["data"]) -> None:
    data: list[dict] = read_file()
    new_item: dict = deepcopy(TEMPLATE)
    new_item["name"] = key
    new_item["description"] = description
    new_item["data"] = profile_data

    data.insert(0, new_item)
    
    with open(FILEPATH, "w") as file:
        json.dump(data, file, indent=4)


def remove_item(key: str) -> None:
    data: list[dict] = read_file()
    new_data: list[dict] = [item for item in data if item.get("name") != key]
    
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
        raise KeyError(f"FastFlag proflie not found in config file: {key}")

    with open(FILEPATH, "w") as file:
        json.dump(data, file, indent=4)


def set_description(key: str, value: str | None) -> None:
    data: list[dict] = read_file()
    
    for i, item in enumerate(data):
        if item.get("name") == key:
            data[i]["description"] = value
            break

    else:
        raise KeyError(f"FastFlag proflie not found in config file: {key}")

    with open(FILEPATH, "w") as file:
        json.dump(data, file, indent=4)


def set_enabled(key: str, value: bool) -> None:
    data: list[dict] = read_file()
    
    for i, item in enumerate(data):
        if item.get("name") == key:
            data[i]["enabled"] = value
            break
    
    else:
        raise KeyError(f"FastFlag proflie not found in config file: {key}")
    
    with open(FILEPATH, "w") as file:
        json.dump(data, file, indent=4)


def set_enabled_studio(key: str, value: bool) -> None:
    data: list[dict] = read_file()
    
    for i, item in enumerate(data):
        if item.get("name") == key:
            data[i]["enabled_studio"] = value
            break
    
    else:
        raise KeyError(f"FastFlag proflie not found in config file: {key}")
    
    with open(FILEPATH, "w") as file:
        json.dump(data, file, indent=4)


def set_data(key: str, value: dict) -> None:
    data: list[dict] = read_file()
    
    for i, item in enumerate(data):
        if item.get("name") == key:
            data[i]["data"] = value
            break

    else:
        raise KeyError(f"FastFlag proflie not found in config file: {key}")

    with open(FILEPATH, "w") as file:
        json.dump(data, file, indent=4)


def read_file() -> list[dict]:
    if not FILEPATH.is_file():
        return []
    
    with open(FILEPATH, "r") as file:
        data: list = json.load(file)
    
    return data