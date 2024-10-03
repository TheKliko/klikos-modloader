from typing import Any
import json

from modules.filesystem import File


def value(key: str, default: Any = None) -> Any:
    with open(File.integrations(), "r") as file:
        data: dict = json.load(file)
    return data.get(key, default)


def get(key: str|None = None) -> dict:
    with open(File.integrations(), "r") as file:
        data: dict = json.load(file)

    if key:
        return data["key"]

    return data


def set(key: str, value: Any) -> None:
    with open(File.integrations(), "r") as file:
        data: dict = json.load(file)

    data[key]["value"] = value

    with open(File.integrations(), "w") as file:
        json.dump(data, file, indent=4)