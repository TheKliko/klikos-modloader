import logging
import sys
import webbrowser

from modules import request
from modules.info import Project, URL
from modules.interface import Color, Response


def check() -> None:
    try:
        url: str = request.Api.latest_version()
        response = request.get(url)
        data: dict = response.json()

        latest_version: str = data['latest']
        current_version: str = Project.VERSION

        if latest_version > current_version:
            print(Color.INFO)
            print("A newer version is avalable!")
            print("Version "+latest_version)
            print(Color.RESET)
            print("Do you wish to update? [Y/N]")
            response = input("Response: ").lower()

            if response in Response.ACCEPT:
                webbrowser.open(URL.LATEST_RELEASE, new=2)
                sys.exit()
            print()

    except Exception as e:
        logging.warning("Failed to check for updates!")
        logging.warning(type(e).__name__+": "+str(e))
        print(Color.WARNING+"- Failed to check for updates!")
        print(Color.ERROR+"  "+type(e).__name__+": "+str(e))


