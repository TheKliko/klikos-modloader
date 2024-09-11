import json
from typing import Any

from modules.other.api import Api
from modules.utils import request


def get(mod: str, default: Any = None) -> dict[str,str]:
    url: str = Api.marketplace()
    response = request.get(url)
    response.raise_for_status()
    data: list[dict[str,str]] = response.json()

    for item in data:
        if item.get('name', None) == mod or item.get('id', None) == mod:
            return item
    
    else:
        return {
            'name': 'BAD_DATA',
            'creator': 'BAD_DATA',
            'description': 'BAD_DATA',
            'id': 'BAD_DATA'
        }


def get_all(default: Any = None) -> list[dict[str,str]]:
    url: str = Api.marketplace()
    response = request.get(url)
    response.raise_for_status()
    data: list[dict[str,str]] = response.json()

    return data