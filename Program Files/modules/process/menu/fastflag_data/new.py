import json

from modules.other.paths import FilePath


def new(profile_name: str) -> None:
    path: str = FilePath.FASTFLAGS
    with open(path, 'r') as file:
        fastflag_profiles: list[dict] = json.load(file)
        file.close()

    data: dict = {'name': profile_name, 'description': None, 'enabled': False, 'data': {}}

    fastflag_profiles.append(data)

    with open(path, 'w') as file:
        json.dump(fastflag_profiles, file, indent=4)
        file.close()