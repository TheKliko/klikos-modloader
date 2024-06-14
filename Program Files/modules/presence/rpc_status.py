"""# rpc_status.py

rpc_status.py is a module used in Kliko's modloader,
it's purpose is to take care of updating the activity status variables used in presence.py.
"""


import glob
import logging
import os
import re
import time

from modules.utils import variables

from modules.utils.request_handler import request


ROBLOX_LOGS: str = os.path.join(os.getenv('LOCALAPPDATA'), 'Roblox', 'Logs')


def update() -> None:
    """Function called to update discord rich presence status"""

    status = read_logs()
    if not status:
        status = [None]

    if 'in_game' in status:  # Playing {game}
        game_id = status[1]
        url = f'https://games.roblox.com/v1/games?universeIds={game_id}'
        game_info = request(url=url)
        game_name = game_info['data'][0]['name']
        game_url = f'https://www.roblox.com/games/{game_info['data'][0]['rootPlaceId']}/'

        game_thumbnail_url = f'https://thumbnails.roblox.com/v1/games/icons?universeIds={game_id}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false'
        game_thumbnail_info = request(url=game_thumbnail_url)
        game_thumbnail = game_thumbnail_info['data'][0]['imageUrl']

        if not variables.get('rpc_playing_timestamp'):
            variables.set(name='rpc_playing_timestamp', value=int(time.time()))
            variables.set(name='rpc_game', value=game_name)
            variables.set(name='rpc_thumbnail', value=game_thumbnail)
            variables.set(
                name='rpc_buttons',
                value=[
                    {
                        "label": "Visit game page",
                        "url": game_url
                    }
                ]
            )
    
    elif 'not_in_roblox' in status:  # 
        variables.set(name='rpc_playing_timestamp', value=None)
        variables.set(name='rpc_game', value=None)
        variables.set(name='rpc_thumbnail', value=None)
        variables.set(
            name='rpc_buttons',
            value=
            [
                {
                    "label": "Learn more",
                    "url": variables.get('website_url')
                }
            ]
        )

        variables.set(name='rpc_details', value='Kliko\'s modloader')
        variables.set(name='rpc_image', value=['launcher', None])
    
    else:  # Roblox Home
        variables.set(name='rpc_playing_timestamp', value=None)
        variables.set(name='rpc_game', value=None)
        variables.set(name='rpc_thumbnail', value=None)
        variables.set(
            name='rpc_buttons',
            value=
            [
                {
                    "label": "Learn more",
                    "url": variables.get('website_url')
                }
            ]
        )
    
    return None


def read_logs() -> list | None:
    try:
        ALL_LOGS = glob.glob(f'{ROBLOX_LOGS}/*')
        LATEST_LOG = max(ALL_LOGS, key=os.path.getmtime)
        with open(LATEST_LOG, 'r') as file:
            data = file.read()
            file.close()

        if '[FLog::SingleSurfaceApp] unregisterMemoryPrioritizationCallback' in data:  # Only exists in logs of closed Roblox instances
            return ['not_in_roblox']

        if not variables.get('rpc_state') == 'playing':
            variables.set(name='rpc_timestamp', value=int(time.time()))
            variables.set(name='rpc_state', value='playing')

        gamejoin: str = '[FLog::GameJoinLoadTime]'
        gameleave: str = '[FLog::SingleSurfaceApp] handleGameWillClose'
        gamejoinleaves: list = [line for line in data.split('\n') if gamejoin in line or gameleave in line]
        if not gamejoinleaves:  # Player is not in-game
            return None

        first_join = True
        for item in gamejoinleaves:
            if gameleave in item:
                first_join = False
        if not first_join:
            i = len(gamejoinleaves) - 1
            while True:
                if i < 0:
                    return None

                if gameleave in gamejoinleaves[i]:
                    pattern = pattern = r'placeid:(\d+)'
                    match = re.search(pattern, gamejoinleaves[i + 1])
                    if not match:
                        return None

                    game_id = match.group(1)
                    return ['in_game', game_id]

                i = i - 1

        else:  # if first_join:
            pattern = pattern = r'universeid:(\d+)'
            match = re.search(pattern, gamejoinleaves[0])
            if not match:
                return None
            
            game_id = match.group(1)
            return['in_game', game_id]

    except Exception as e:
        logging.error(f'A {type(e).__name__} occured while reading Roblox logs to update RPC status')
        logging.debug(e)

    return None



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()