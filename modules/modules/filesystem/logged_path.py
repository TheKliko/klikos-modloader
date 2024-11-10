import os

from .directories import Directory


USERPROFILE: str | None = os.getenv("HOME") or os.getenv("USERPROFILE")
APPDATA: str | None = os.getenv("APPDATA")
LOCALAPPDATA: str | None = os.getenv("LOCALAPPDATA")
TEMP: str | None = os.getenv("TEMP")


def get(path: str) -> str:
    ROOT: str = Directory.root()
    
    logged_path: str = path
    logged_path = logged_path.replace(ROOT, r"{ROOT}")
    if TEMP:
        logged_path = logged_path.replace(TEMP, r"%TEMP%")
    if LOCALAPPDATA:
        logged_path = logged_path.replace(LOCALAPPDATA, r"%LOCALAPPDATA%")
    if APPDATA:
        logged_path = logged_path.replace(APPDATA, r"%APPDATA%")
    if USERPROFILE:
        logged_path = logged_path.replace(USERPROFILE, r"%USERPROFILE%")
    
    return logged_path