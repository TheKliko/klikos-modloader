import os

from .directories import Directory


def get(path: str) -> str:
    USERPROFILE: str = os.getenv("USERPROFILE")
    APPDATA: str = os.getenv("APPDATA")
    LOCALAPPDATA: str = os.getenv("LOCALAPPDATA")
    TEMP: str = os.getenv("TEMP")
    ROOT: str = Directory.root()
    
    logged_path: str = path
    if ROOT:
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