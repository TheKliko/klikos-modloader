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