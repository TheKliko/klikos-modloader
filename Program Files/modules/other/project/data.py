import os


class Project:
    NAME: str = 'Kliko\'s modloader'
    DESCRIPTION: str = 'Roblox mods made easy'
    AUTHOR: str = 'TheKliko'
    VERSION: str = '1.4.0-dev'
    ICON: str = os.path.join(os.path.dirname(__file__), 'favicon.ico')