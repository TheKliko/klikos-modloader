from typing import Any
import json
import logging
import copy

from modules.filesystem import File


def get(key: str|None = None) -> list|dict|None:
    with open(File.mods(), "r") as file:
        data: list = json.load(file)

    if key:
        for item in data:
            if item["name"] == key:
                return item
        else:
            return None

    return data


def set(name: str, key: str, value: Any) -> None:
    with open(File.mods(), "r") as file:
        data: list = json.load(file)

    old_data = copy.deepcopy(data)

    for i, profile in enumerate(data):
        if profile["name"] == name:
            data[i][key] = value

    try:
        with open(File.mods(), "w") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        with open(File.mods(), "w") as file:
            json.dump(old_data, file, indent=4)

        logging.error(type(e).__name__+": "+str(e))
        raise


def rename_profile(old: str, new: str) -> None:
    set(name=old, key="name", value=new)


def delete_profile(name: str) -> None:
    with open(File.mods(), "r") as file:
        data: list = json.load(file)
    old_data = copy.deepcopy(data)

    for i, item in enumerate(data):
        if item["name"] == name:
            data.pop(i)
            break
    else:
        return

    try:
        with open(File.mods(), "w") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        with open(File.mods(), "w") as file:
            json.dump(old_data, file, indent=4)

        logging.error(type(e).__name__+": "+str(e))
        raise


def create_profile(profile_data: dict) -> None:
    with open(File.mods(), "r") as file:
        data: list = json.load(file)
    old_data = copy.deepcopy(data)
    
    data.insert(0, profile_data)

    try:
        with open(File.mods(), "w") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        with open(File.mods(), "w") as file:
            json.dump(old_data, file, indent=4)

        logging.error(type(e).__name__+": "+str(e))
        raise