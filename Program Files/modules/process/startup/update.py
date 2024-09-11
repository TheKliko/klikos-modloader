import webbrowser

from modules.interface import Print, Color, Interface
from modules.other.api import Api
from modules.other.hyperlinks import Hyperlink
from modules.other.project import Project
from modules.other.response import Response
from modules.process.shutdown.exceptions import ManualQuitOut
from modules.utils.request import request


def check_for_updates() -> None:
    try:
        Print('Checking for updates . . .', color=Color.INITALIZE)
        url: str = Api.latest_version()
        response = request.get(url)

        data: dict = response.json()
        latest_version: str = data['latest']

        if latest_version > Project.VERSION:
            interface = Interface('An update is available!', f'Version: {latest_version}')
            interface.add_line('Do you wish to install this version? [Y/N]')
            interface.add_divider()
            response = interface.get_input('Response: ')

            if response in Response.DENY:
                return
            
            webbrowser.open(Hyperlink.LATEST_RELEASE, new=2)
            raise ManualQuitOut('User chose to update this program')

    except Exception as e:
        Print(f'- Failed to check for updates! [{type(e).__name__}] {str(e)}', color=Color.WARNING, indent = 2)