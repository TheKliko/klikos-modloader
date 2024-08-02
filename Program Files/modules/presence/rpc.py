import logging
import os
import time

from libraries.pypresence import Presence, DiscordNotFound, PipeClosed

from modules.presence import activity
from modules.presence.status import RichPresenceStatus
from modules.utils import json_manager
from modules.utils import variables


CLIENT_ID: str = '1229494846247665775'
rpc = Presence(CLIENT_ID)


class RichPresenceImage():
    LAUNCHER_LARGE: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/launcher.png'
    LAUNCHER_SMALL: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/launcher-small.png'
    MENU_LARGE: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/menu.png'
    MENU_SMALL: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/menu-small.png'
    ROBLOX: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/roblox.png'
    STUDIO: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/studio.png'
    WARNING: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/warning.png'


def start() -> None:
    """Start Discord rich presence"""

    DISCORD_RPC: bool = variables.get('discord_rpc')
    if not DISCORD_RPC:
        return

    logging.info('Starting rich presence')

    connect()


def connect() -> None:
    """Connect the client and send status updates"""

    try:
        rpc.connect()
        while True:
            if variables.get('rpc_stopped'):
                return

            update()

            time.sleep(2)

    except DiscordNotFound:
        logging.warning('Discord not found. Retrying in 15 seconds')
        time.sleep(15)
        start()

    except PipeClosed:
        logging.warning('Discord pipe closed. Retrying in 15 seconds')
        time.sleep(15)
        start()
    
    except Exception as e:
        logging.error(f'[RichPresenceError] An unexpected ({type(e).__name__}) occured: {str(e)}')


def update() -> None:
    """Update rpc status"""

    PROJECT_DATA: dict = variables.get('project_data')
    def default_values() -> tuple:
        details = PROJECT_DATA['name']
        state = None
        large_image = RichPresenceImage.MENU_LARGE
        large_text = 'Modloader Menu'
        small_image = RichPresenceImage.LAUNCHER_SMALL
        small_text = PROJECT_DATA['name']
        timestamp = None
        return details, state, large_image, large_text, small_image, small_text, timestamp

    details, state, large_image, large_text, small_image, small_text, timestamp = default_values()

    STATUS: str = activity.update() or variables.get('rpc_status')

    if STATUS == RichPresenceStatus.MENU:
        details = 'Modloader Menu'
        state = variables.get('rpc_state') or f'v{PROJECT_DATA['version']}'
        large_image = RichPresenceImage.MENU_LARGE
        large_text = 'Modloader Menu'
        small_image = RichPresenceImage.LAUNCHER_SMALL
        small_text = PROJECT_DATA['name']
        timestamp = None

    elif STATUS == RichPresenceStatus.LAUNCHER:
        details = 'Launcher'
        state = variables.get('rpc_state')
        large_image = RichPresenceImage.LAUNCHER_LARGE
        large_text = PROJECT_DATA['name']
        small_image = None
        small_text = None
        timestamp = None

    elif STATUS == RichPresenceStatus.ERROR:
        details = variables.get('rpc_details')
        state = variables.get('rpc_state')
        large_image = RichPresenceImage.WARNING
        large_text = 'An error occured'
        small_image = RichPresenceImage.LAUNCHER_SMALL
        small_text = PROJECT_DATA['name']
        timestamp = None

    elif STATUS == RichPresenceStatus.PLAYING:
        details = 'Roblox Player'
        state = f'Playing {variables.get('rpc_name')}'
        large_image = variables.get('rpc_image')
        large_text = variables.get('rpc_game')
        small_image = RichPresenceImage.ROBLOX
        small_text = 'Roblox'
        timestamp = variables.get('rpc_timestamp')

    elif STATUS == RichPresenceStatus.CREATING:
        details = 'Roblox Studio'
        state = f'Editing {variables.get('rpc_name')}'
        large_image = variables.get('rpc_image')
        large_text = variables.get('rpc_game')
        small_image = RichPresenceImage.STUDIO
        small_text = 'Roblox Studio'
        timestamp = variables.get('rpc_timestamp')

    elif STATUS == RichPresenceStatus.ROBLOX:
        details = 'Playing Roblox'
        state = None
        large_image = RichPresenceImage.ROBLOX
        large_text = 'Roblox'
        small_image = RichPresenceImage.LAUNCHER_SMALL
        small_text = PROJECT_DATA['name']
        timestamp = None

    elif STATUS == RichPresenceStatus.STUDIO:
        details = 'Playing Roblox Studio'
        state = None
        large_image = RichPresenceImage.STUDIO
        large_text = 'Roblox Studio'
        small_image = RichPresenceImage.LAUNCHER_SMALL
        small_text = PROJECT_DATA['name']
        timestamp = None

    rpc.update(
        details=details,
        state=state,
        large_image=large_image,
        large_text=large_text,
        small_image=small_image,
        small_text=small_text,
        start=timestamp
    )


def stop(attempt: int = 0, retries: int = 5) -> None:
    DISCORD_RPC: bool = variables.get('discord_rpc')
    if not DISCORD_RPC:
        return
    
    logging.info('Stopping rich presence')
    variables.set('rpc_stopped', True)
    if attempt < retries:
        try:
            rpc.close()
        
        except (AssertionError, RuntimeError):
            attempt += 1
            stop(attempt)
    
    else:
        logging.warning('Failed to stop rich presence')


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()