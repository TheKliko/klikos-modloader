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

class RobloxApi:
    pass