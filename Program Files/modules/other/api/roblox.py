class RobloxApi:
    @classmethod
    def user_channel(cls, binary_type: str):
        return rf'https://clientsettings.roblox.com/v2/user-channel?binaryType={binary_type}'

    @classmethod
    def latest_version(cls, binary_type: str, channel: str = None):
        if channel:
            return rf'https://clientsettingscdn.roblox.com/v2/client-version/{binary_type}/channel/{channel}'
        return rf'https://clientsettingscdn.roblox.com/v2/client-version/{binary_type}'
    
    @classmethod
    def roblox_package_manifest(cls, version: str):
        return rf'https://setup.rbxcdn.com/{version}-rbxPkgManifest.txt'
    
    @classmethod
    def file_download(cls, version: str, file: str):
        return rf'https://setup.rbxcdn.com/{version}-{file}'
    
    @classmethod
    def deploy_history(cls):
        return r'https://setup.rbxcdn.com/DeployHistory.txt'
    
    @classmethod
    def game_universe_id(cls, place_id: str):
        return rf'https://apis.roblox.com/universes/v1/places/{place_id}/universe'
    
    @classmethod
    def game_info(cls, universe_id: str):
        return rf'https://games.roblox.com/v1/games?universeIds={universe_id}'
    
    @classmethod
    def game_thumbnail(cls, universe_id: str, size: str = '512x512', circular: bool = False):
        return rf'https://thumbnails.roblox.com/v1/games/icons?universeIds={universe_id}&returnPolicy=PlaceHolder&size={size}&format=Png&isCircular={str(circular).lower()}'