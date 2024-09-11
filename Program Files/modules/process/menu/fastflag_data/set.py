import json
from typing import Any, Literal

from modules.other.paths import FilePath


def set(profile_name: str, value: str|list|bool|dict|None, type: Literal['name','description','enabled','data-add','data-remove'] = None) -> None:
    path: str = FilePath.FASTFLAGS
    with open(path, 'r') as file:
        fastflag_profiles: list[dict] = json.load(file)
        file.close()

    for i, item in enumerate(fastflag_profiles):
        if item.get('name', None) == profile_name:
            data: dict = fastflag_profiles.pop(i)
            index = i
            break
    else:
        data = {'name': profile_name, 'description': None, 'enabled': False, data: {}}
        index = 0

    if type == 'name':
        data['name'] = value
    elif type == 'description':
        data['description'] = value
    elif type == 'enabled':
        data['enabled'] = value
    elif type == 'data-add' and isinstance(value, dict):
        for k, v in value.items():
            data['data'][k] = v
    elif type == 'data-remove':
        data['data'].pop(value, None)

    fastflag_profiles.insert(index, data)

    with open(path, 'w') as file:
        json.dump(fastflag_profiles, file, indent=4)
        file.close()