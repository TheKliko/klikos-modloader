import logging
import re

from modules.other.api import RobloxApi
from modules.utils import request


def get_manifest(version: str) -> list[str]:
    try:
        url: str = RobloxApi.roblox_package_manifest(version)
        response = request.get(url)
        data: str = response.text
        
        manifest: list[str] = re.findall(r'\b\S+\.zip\b', data) + re.findall(r'\b\S+\.exe\b', data)  # Only extract .zip or .exe files

        # re.findall(r'\b\S+\.zip\b', data)  # Only extract .zip files
        # re.findall(r'\b\S+\.(zip|exe)\b', data)  # Only extract .zip or .exe files
        # re.findall(r'\b\S+\.\S+\b', data)  # Extract all files

        return manifest

    except Exception as e:
        logging.error(f'[{type(e).__name__}] {str(e)}')
        raise type(e)(str(e))