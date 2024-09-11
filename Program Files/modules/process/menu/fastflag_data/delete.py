import json

from modules.other.paths import FilePath


def delete(profile_name: str) -> None:
    path: str = FilePath.FASTFLAGS
    with open(path, 'r') as file:
        fastflag_profiles: list[dict] = json.load(file)
        file.close()

    for i, item in enumerate(fastflag_profiles):
        if item.get('name', None) == profile_name:
            fastflag_profiles.pop(i)
            break

    with open(path, 'w') as file:
        json.dump(fastflag_profiles, file, indent=4)
        file.close()