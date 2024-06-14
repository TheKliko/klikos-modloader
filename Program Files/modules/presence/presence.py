"""# presence.py

presence.py is a module used in Kliko's modloader,
it's purpose is to take care of starting, updating and stopping discord rich presence.
"""


import logging
import os
import time

from modules.presence import rpc_status
from modules.utils import variables

from packages.pypresence import Presence, DiscordNotFound, PipeClosed


CLIENT_ID: str = '1229494846247665775'
IMAGE_LAUNCHER_LARGE: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/launcher.png'
IMAGE_LAUNCHER_SMALL: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/launcher-small.png'
IMAGE_MENU_LARGE: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/menu.png'
IMAGE_MENU_SMALL: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/menu-small.png'
IMAGE_ROBLOX: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/roblox.png'
IMAGE_STUDIO: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/GitHub%20Files/rpc-images/studio.png'

rpc = Presence(CLIENT_ID)


def start() -> None:
    """Function called to start discord rich presence"""

    logging.info('Starting rich presence...')

    try:
        if variables.get('discord_rpc') and not variables.get_silent('rpc_active'):
            connect()

    except DiscordNotFound as e:
        logging.warning(f'Discord not found!')
        logging.info(f'Retrying in 15 seconds')
        time.sleep(15)
        start()
    
    except PipeClosed as e:
        logging.warning(f'Discord pipe closed!')
        logging.info(f'Retrying in 5 seconds')
        time.sleep(5)
        variables.set(name='rpc_active', value=False)
        start()

    except Exception as e:
        logging.error('An error occured during rich presence.')
        logging.debug(f'{type(e).__name__}: {str(e)}')
        variables.set(name='rpc_end', value=True)
        variables.set(name='rpc_active', value=False)


def stop() -> None:
    """Function called to stop discord rich presence"""

    logging.info('Stopping rich presence...')
    if variables.get('discord_rpc'):
        try:
            rpc.close()
        except (AssertionError, RuntimeError):
            pass

    variables.set(name='rpc_end', value=True)
    variables.set(name='rpc_active', value=False)


def connect() -> None:
    rpc.connect()
    variables.set(name='rpc_active', value=True)
    while not variables.get_silent('rpc_end'):
        STATE: str = variables.get('rpc_state')
        if STATE == 'launcher' or STATE == 'playing':
            rpc_status.update()
        update()
        time.sleep(2)
    stop()
    variables.set(name='rpc_active', value=False)


def update() -> None:
    STATE: str = variables.get('rpc_state')
    PROGRAM_NAME: str = variables.get('project_name')

    timestamp = variables.get('rpc_timestamp')
    buttons = variables.get('rpc_buttons')
    state = None

    logging.info(f'Updating rpc status: {STATE}')
    
    if STATE == 'startup':
        large_image = IMAGE_LAUNCHER_LARGE
        large_text = 'Kliko\'s modloader'
        small_image = None
        small_text = None
        details = 'Initializing...'
    
    elif STATE == 'error':
        large_image = IMAGE_MENU_LARGE
        large_text = 'Modloader menu'
        small_image = IMAGE_LAUNCHER_SMALL
        small_text = PROGRAM_NAME
        details = 'An error occured...'
        timestamp = None
        error_type = variables.get_silent('error_type')
        if error_type:
            state = f'Type: {error_type}'
    
    elif STATE == 'shutdown':
        large_image = IMAGE_MENU_LARGE
        large_text = 'Modloader menu'
        small_image = IMAGE_LAUNCHER_SMALL
        small_text = PROGRAM_NAME
        details = 'Terminating...'
    
    elif STATE == 'playing':
        rpc_playing_timestamp = variables.get('rpc_playing_timestamp')
        if rpc_playing_timestamp:
            timestamp = variables.get('rpc_playing_timestamp')
            rpc_game = variables.get('rpc_game')
            rpc_thumbnail = variables.get('rpc_thumbnail')
            details = f'Playing {rpc_game}'
            large_image = rpc_thumbnail
            large_text = rpc_game
            small_image = IMAGE_LAUNCHER_SMALL
            small_text = PROGRAM_NAME
            small_image = IMAGE_ROBLOX
            small_text = 'Roblox'

        else:
            large_image = IMAGE_ROBLOX
            large_text = 'Roblox'
            small_image = IMAGE_LAUNCHER_SMALL
            small_text = PROGRAM_NAME
            details = 'Playing Roblox'
    
    elif STATE == 'launcher':
        large_image = IMAGE_LAUNCHER_LARGE
        large_text = PROGRAM_NAME
        small_image = None
        small_text = None
        details = 'Launching Roblox...'

    elif STATE == 'menu':
        large_image = IMAGE_MENU_LARGE
        large_text = 'Modloader menu'
        small_image = IMAGE_LAUNCHER_SMALL
        small_text = PROGRAM_NAME
        details = 'Modloader menu'
    
    elif STATE == 'studio':
        large_image = IMAGE_STUDIO
        large_text = 'Roblox Studio'
        small_image = IMAGE_LAUNCHER_SMALL
        small_text = PROGRAM_NAME
        details = 'Roblox Studio'

    rpc.update(
        details=details,
        state=state,
        start=timestamp,
        large_image=large_image,
        large_text=large_text,
        small_image=small_image,
        small_text=small_text,
        buttons=buttons
    )


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()