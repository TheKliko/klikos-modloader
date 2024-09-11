import json
from typing import Any

from modules.other.paths import FilePath


def get(setting: str, default: Any = None) -> Any:
    path: str = FilePath.SETTINGS
    with open(path, 'r') as file:
        settings: dict = json.load(file)
        file.close()

    for key, value in settings.items():
        if value.get('name', None) == setting:
            return value

    return settings.get(setting, default)


def get_all(default: Any = None) -> Any:
    path: str = FilePath.SETTINGS
    with open(path, 'r') as file:
        settings: dict = json.load(file)
        file.close()

    return settings