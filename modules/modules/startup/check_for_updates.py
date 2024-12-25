import sys
import json
from tkinter import messagebox
import webbrowser

from modules import Logger
from modules.info import ProjectData, Help
from modules import request
from modules.request import Api, Response


def check_for_updates() -> None:
    latest_version: str = get_latest_version()
    if latest_version <= ProjectData.VERSION:
        return
    
    Logger.debug(f"A newer version is available: {latest_version}")
    if not messagebox.askokcancel(title=ProjectData.NAME, message=f"A newer version is available: Version {latest_version}\nDo you wish to update?"):
        Logger.warning("Update cancelled!")
        return
    
    Logger.info("User chose to update!")
    webbrowser.open(Help.LATEST_VERSION)
    sys.exit()


def get_latest_version() -> str:
    response: Response = request.get(Api.GitHub.LATEST_VERSION)
    data: dict = response.json()
    version: str = data["latest"]
    return version