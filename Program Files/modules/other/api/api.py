class Api:
    @classmethod
    def latest_version(cls):
        return r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub Files/version.json'

    @classmethod
    def ip_info(cls, ip: str):
        return rf'https://ipinfo.io/{ip}/json'
    
    @classmethod
    def country_name(cls, code: str):
        return rf'https://restcountries.com/v3.1/alpha/{code}'
    
    @classmethod
    def marketplace(cls, mod_id: str = None):
        if mod_id is None:
            return r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/remote-mod-downloads/index.json'
        return rf'https://github.com/TheKliko/klikos-modloader/raw/remote-mod-downloads/mods/{mod_id}.zip'