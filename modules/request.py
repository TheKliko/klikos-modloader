import time
from typing import Literal, Optional

from modules.logger import logger

import requests
from requests import Response


COOLDOWN: int = 2
_cache: dict = {}


class RequestError(Exception):
    pass


# region GitHubApi
class GitHubApi:
    @staticmethod
    def latest_version() -> str:
        return r"https://raw.githubusercontent.com/TheKliko/klikos-modding-tool/refs/heads/main/GitHub%20Files/version.json"
    
    @staticmethod
    def marketplace() -> str:
        return r"https://raw.githubusercontent.com/TheKliko/klikos-modding-tool/refs/heads/remote-mod-download/index.json"
    
    @staticmethod
    def mod_thumbnail(mod_id: str) -> str:
        return rf"https://raw.githubusercontent.com/TheKliko/klikos-modding-tool/refs/heads/remote-mod-download/thumbnails/{mod_id}.png"
    
    @staticmethod
    def mod_download(mod_id: str) -> str:
        return rf"https://raw.githubusercontent.com/TheKliko/klikos-modding-tool/refs/heads/remote-mod-download/mods/{mod_id}.zip"


# region RobloxApi
class RobloxApi:
    @staticmethod
    def user_channel(binary_type: Literal["WindowsPlayer", "WindowsStudio"]) -> str:
        return rf"https://clientsettings.roblox.com/v2/user-channel?binaryType={binary_type}"
    
    @staticmethod
    def latest_version(binary_type: Literal["WindowsPlayer", "WindowsStudio"], user_channel: Optional[str] = None) -> str:
        if not user_channel:
            return rf"https://clientsettingscdn.roblox.com/v2/client-version/{binary_type}"
        return rf"https://clientsettingscdn.roblox.com/v2/client-version/{binary_type}/channel/{user_channel}"

    @staticmethod
    def deploy_history() -> str:
        return r"https://setup.rbxcdn.com/DeployHistory.txt"
    
    @staticmethod
    def download(version: str, file: str) -> str:
        return rf"https://setup.rbxcdn.com/{version}-{file}"


# region get()
def get(url, attempts: int = 3, cache: bool = False) -> Response:
    if cache:
        if url in _cache:
            logger.debug(f"Cached GET request: {url}")
            return _cache[url]

    attempts -= 1

    try:
        logger.info(f"Attempting GET request: {url}")
        response: Response = requests.get(url, timeout=(5,15))
        response.raise_for_status()
        _cache[url] = response
        return response

    except Exception as e:
        logger.error(f"GET request failed: {url}, reason: {type(e).__name__}: {e}")

        if attempts <= 0:
            logger.error(f"GET request failed: {url}, reason: Too many attempts!")
            raise
        
        logger.warning(f"Remaining attempts: {attempts}")
        logger.info(f"Retrying in {COOLDOWN} seconds...")
        time.sleep(COOLDOWN)
        return get(url=url, attempts=attempts, cache=cache)