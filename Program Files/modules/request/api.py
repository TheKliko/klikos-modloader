class Api:
    @staticmethod
    def latest_version() -> str:
        return r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/version-1.5.0/GitHub%20Files/version.json"
    

    @staticmethod
    def marketplace() -> str:
        return r"https://raw.githubusercontent.com/TheKliko/klikos-modloader/refs/heads/remote-mod-downloads/index.json"
    

    @staticmethod
    def mod_thumbnail(id: str) -> str:
        return r"https://github.com/TheKliko/klikos-modloader/raw/remote-mod-downloads/thumbnails/"+id+".png"
    

    @staticmethod
    def mod_download(id: str) -> str:
        return r"https://github.com/TheKliko/klikos-modloader/raw/remote-mod-downloads/mods/"+id+".zip"


class RobloxApi:
    @staticmethod
    def user_channel(binary_type: str = "WindowsPlayer") -> str:
        return r"https://clientsettings.roblox.com/v2/user-channel?binaryType="+binary_type
    

    @staticmethod
    def latest_version(binary_type: str = "WindowsPlayer", user_channel: str|None = None) -> str:
        if not user_channel:
            return r"https://clientsettingscdn.roblox.com/v2/client-version/"+binary_type
        return r"https://clientsettingscdn.roblox.com/v2/client-version/"+binary_type+r"/channel/"+user_channel
    

    @staticmethod
    def deploy_history() -> str:
        return r"https://setup.rbxcdn.com/DeployHistory.txt"
    

    @staticmethod
    def download(version: str, file: str) -> str:
        return r"https://setup.rbxcdn.com/"+version+"-"+file
    

    @staticmethod
    def fastflags() -> str:
        return r"https://clientsettingscdn.roblox.com/v2/settings/application/PCDesktopClient"
    
    @classmethod
    def game_universe_id(cls, place_id: str):
        return r"https://apis.roblox.com/universes/v1/places/"+place_id+r"/universe"
    
    @classmethod
    def game_info(cls, universe_id: str):
        return r"https://games.roblox.com/v1/games?universeIds="+universe_id
    
    @classmethod
    def game_thumbnail(cls, universe_id: str, size: str = "512x512", circular: bool = False):
        return r"https://thumbnails.roblox.com/v1/games/icons?universeIds="+universe_id+r"&returnPolicy=PlaceHolder&size="+size+r"&format=Png&isCircular="+str(circular).lower()
    
    @classmethod
    def game_page(cls, root_place_id: str):
        return r"https://www.roblox.com/games/"+root_place_id
    
    @classmethod
    def game_join(cls, root_place_id: str, job_id: str):
        return r"roblox://experiences/start?placeId="+root_place_id+r"&gameInstanceId="+job_id
    
    @classmethod
    def game_asset(cls, asset_id: str):
        return r"https://assetdelivery.roblox.com/v1/asset/?id="+asset_id