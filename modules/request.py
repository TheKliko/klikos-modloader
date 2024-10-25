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
        return r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/main/GitHub%20Files/version.json"
    
    @staticmethod
    def marketplace() -> str:
        return r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/remote-mod-downloads/index.json"
    
    @staticmethod
    def mod_thumbnail(mod_id: str) -> str:
        return rf"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/remote-mod-downloads/thumbnails/{mod_id}.png"
    
    @staticmethod
    def mod_download(mod_id: str) -> str:
        return rf"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/remote-mod-downloads/mod/{mod_id}.zip"
    
    @staticmethod
    def fastflag_presets() -> str:
        return r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/fastflag-presets/index.json"


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
    
    @staticmethod
    def fastflags() -> str:
        return r"https://clientsettingscdn.roblox.com/v2/settings/application/PCDesktopClient"


# region RobloxActivityApi
class RobloxActivityApi:
    @staticmethod
    def game_universe_id(place_id: str) -> str:
        return rf"https://apis.roblox.com/universes/v1/places/{place_id}/universe"
    
    @staticmethod
    def game_info(universe_id: str) -> str:
        return rf"https://games.roblox.com/v1/games?universeIds={universe_id}"
    
    @staticmethod
    def game_thumbnail(universe_id: str, size: str = "512x512", circular: bool = False) -> str:
        return rf"https://thumbnails.roblox.com/v1/games/icons?universeIds={universe_id}&returnPolicy=PlaceHolder&size={size}&format=Png&isCircular={str(circular).lower()}"
    
    @staticmethod
    def game_page(root_place_id: str) -> str:
        return rf"https://www.roblox.com/games/{root_place_id}"
    
    @staticmethod
    def game_join(root_place_id: str, job_id: str) -> str:
        return rf"roblox://experiences/start?placeId={root_place_id}&gameInstanceId={job_id}"
    
    @staticmethod
    def game_asset(asset_id: str) -> str:
        return rf"https://assetdelivery.roblox.com/v1/asset/?id={asset_id}"


# region get()
def get(url, attempts: int = 3, cache: bool = False) -> Response:
    if cache:
        if url in _cache:
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