from typing import Optional
import time

from modules import Logger

import requests
from requests import Response, ConnectionError


COOLDOWN: float = 2
TIMEOUT: tuple[int,int] = (5,15)
_cache: dict = {}


# region APIs
class Api:
    class GitHub:
        LATEST_VERSION: str = r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/main/GitHub%20Files/version.json"
        RELEASE_INFO: str = r"https://api.github.com/repos/thekliko/klikos-modloader/releases/latest"
        FILEMAP: str = r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/config/filemap.json"
        FASTFLAG_PRESETS: str = r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/config/fastflag_presets.json"
        MARKETPLACE: str = r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/remote-mod-downloads/index.json"
        @staticmethod
        def mod_thumbnail(id: str) -> str:
            return rf"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/remote-mod-downloads/thumbnails/{id}.png"
        @staticmethod
        def mod_download(id: str) -> str:
            return rf"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/remote-mod-downloads/mods/{id}.zip"
    
    class Roblox:
        FASTFLAGS: str = r"https://clientsettingscdn.roblox.com/v2/settings/application/PCDesktopClient"

        class Deployment:
            HISTORY: str = r"https://setup.rbxcdn.com/DeployHistory.txt"
            @staticmethod
            def channel(binaryType: str) -> str:
                return rf"https://clientsettings.roblox.com/v2/user-channel?binaryType={binaryType}"
            @staticmethod
            def latest(binaryType: str, channel: Optional[str] = None) -> str:
                if channel is None:
                    rf"https://clientsettingscdn.roblox.com/v2/client-version/{binaryType}"
                return rf"https://clientsettingscdn.roblox.com/v2/client-version/{binaryType}/channel/{channel}"
            @staticmethod
            def manifest(version: str) -> str:
                return rf"https://setup.rbxcdn.com/{version}-rbxPkgManifest.txt"
            @staticmethod
            def download(version: str, file: str) -> str:
                return rf"https://setup.rbxcdn.com/{version}-{file}"

        class Activity:
            @staticmethod
            def universe_id(placeId: str) -> str:
                return rf"https://apis.roblox.com/universes/v1/places/{placeId}/universe"
            @staticmethod
            def game(universeId: str) -> str:
                return rf"https://games.roblox.com/v1/games?universeIds={universeId}"
            @staticmethod
            def thumbnail(universeId: str, size: str = "512x512", isCircular: bool = False) -> str:
                return rf"https://thumbnails.roblox.com/v1/games/icons?universeIds={universeId}&returnPolicy=PlaceHolder&size={size}&format=Png&isCircular={str(isCircular).lower()}"
            @staticmethod
            def asset(assetId: str) -> str:
                return rf"https://assetdelivery.roblox.com/v1/asset/?id={assetId}"
            @staticmethod
            def page(rootPlaceId: str) -> str:
                return rf"https://www.roblox.com/games/{rootPlaceId}"
            @staticmethod
            def deeplink(placeId: str, gameInstanceId: str) -> str:
                return rf"roblox://experiences/start?placeId={placeId}&gameInstanceId={gameInstanceId}"
            @staticmethod
            def user(userId: str) -> str:
                return rf"https://users.roblox.com/v1/users/{userId}"


# region get()
def get(url: str, attempts: int = 3, cached: bool = False, timeout: Optional[tuple[int, int]] = None) -> Response:
    if cached and url in _cache:
        Logger.info(f"Cached GET request: {url}")
        return _cache[url]
    
    exception: Exception | None = None

    for _ in range(attempts):
        try:
            Logger.info(f"GET request: {url}")
            response: Response = requests.get(url, timeout=timeout or TIMEOUT)
            response.raise_for_status()
            _cache[url] = response
            return response

        except Exception as e:
            Logger.error(f"GET request failed! {type(e).__name__}: {e}")
            exception = e
            time.sleep(COOLDOWN)
    
    if exception is not None:
        raise exception