from typing import Any
import json
import logging
import copy

from modules.filesystem import File


def value(key: str, default: Any = None) -> Any:
    with open(File.integrations(), "r") as file:
        data: dict = json.load(file)
    return data.get(key, {}).get("value", default)


def get(key: str|None = None) -> dict:
    with open(File.integrations(), "r") as file:
        data: dict = json.load(file)

    if key:
        return data["key"]

    return data


def set(key: str, value: Any) -> None:
    with open(File.integrations(), "r") as file:
        data: dict = json.load(file)

    old_data = copy.deepcopy(data)
    data[key]["value"] = value

    try:
        with open(File.integrations(), "w") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        with open(File.integrations(), "w") as file:
            json.dump(old_data, file, indent=4)

        logging.error(type(e).__name__+": "+str(e))
        raise