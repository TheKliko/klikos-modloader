from typing import Any
import json
import logging
import copy

from modules.filesystem import File


def value(name: str, default: Any = None) -> Any:
    with open(File.fastflags(), "r") as file:
        data: list = json.load(file)

    for profile in data:
        if profile["name"] == name:
            return profile


def get(key: str|None = None) -> list:
    with open(File.fastflags(), "r") as file:
        data: list = json.load(file)

    if key:
        for item in data:
            if item["name"] == key:
                return item

    return data


def set(name: str, key: str, value: Any) -> None:
    with open(File.fastflags(), "r") as file:
        data: list = json.load(file)

    old_data = copy.deepcopy(data)

    for i, profile in enumerate(data):
        if profile["name"] == name:
            data[i][key] = value

    try:
        with open(File.fastflags(), "w") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        with open(File.fastflags(), "w") as file:
            json.dump(old_data, file, indent=4)

        logging.error(type(e).__name__+": "+str(e))
        raise type(e)(str(e))