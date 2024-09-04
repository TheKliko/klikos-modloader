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