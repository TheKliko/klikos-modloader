import json
from typing import Any

from modules.other.paths import FilePath


def set(itnegration: str, value: Any) -> None:
    path: str = FilePath.INTEGRATIONS
    with open(path, 'r') as file:
        itnegrations: dict = json.load(file)
        file.close()
    
    itnegrations[itnegration]['value'] = value

    with open(path, 'w') as file:
        json.dump(itnegrations, file, indent=4)
        file.close()