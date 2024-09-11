import json

from modules.other.paths import FilePath


def set(setting: str, value: bool|int) -> None:
    path: str = FilePath.SETTINGS
    with open(path, 'r') as file:
        settings: dict = json.load(file)
        file.close()

    for key, data in settings.items():
        if data.get('name', None) == setting:
            setting = key
            break
    
    settings[setting]['value'] = value

    with open(path, 'w') as file:
        json.dump(settings, file, indent=4)
        file.close()