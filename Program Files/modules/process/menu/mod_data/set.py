import json
from typing import Any

from modules.other.paths import FilePath


def set(mod: str, value: int|bool) -> None:
    path: str = FilePath.MODS
    with open(path, 'r') as file:
        mods: list[dict] = json.load(file)
        file.close()

    for i, item in enumerate(mods):
        if item.get('name', None) == mod:
            data: dict = mods.pop(i)
            index = i
            break
    else:
        data = {'name': mod, 'enabled': False, 'priority': 0}
        index = 0

    if type(value) == bool:
        data['enabled'] = value
    elif isinstance(value, int):
        data['priority'] = value

    mods.insert(index, data)

    with open(path, 'w') as file:
        json.dump(mods, file, indent=4)
        file.close()