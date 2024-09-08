import json
from typing import Any

from modules.other.paths import FilePath


def set(setting: str, value: Any) -> None:
    path: str = FilePath.SETTINGS
    with open(path, 'r') as file:
        settings: dict = json.load(file)
        file.close()
    
    settings[setting]['value'] = value

    with open(path, 'w') as file:
        json.dump(settings, file, indent=4)
        file.close()