import json
from typing import Any

from modules.other.paths import FilePath


def get(integration: str, default: Any = None) -> Any:
    path: str = FilePath.INTEGRATIONS
    with open(path, 'r') as file:
        integrations: dict = json.load(file)
        file.close()

    return integrations.get(integration, default)