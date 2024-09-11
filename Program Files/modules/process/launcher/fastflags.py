import json
import logging
import os
from typing import Any

from modules.other.paths import FilePath, Directory
from modules.utils import filesystem


def apply(version: str) -> None:
    logging.info('Applying fastflags')


    fastflags_file: str = FilePath.FASTFLAGS
    with open(fastflags_file, 'r') as file:
        config: list[dict[str, Any]] = json.load(file)
        file.close()
    
    version_directory: str = os.path.join(Directory.VERSIONS, version)
    save_path: str = os.path.join(version_directory, 'ClientSettings', 'ClientAppSettings.json')
    filesystem.verify(os.path.dirname(save_path), create_missing_directories=True)
    data: dict[str, Any] = {}

    for profile in config:
        is_enabled: bool = profile.get('enabled', False)
        if is_enabled == False:
            continue
        
        fastflags: dict = profile.get('data', {})
        if fastflags == {}:
            continue

        for key, value in fastflags.items():
            data[key] = value

    with open(save_path, 'w') as file:
        json.dump(data, file)
        file.close()