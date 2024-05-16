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
        url = 'https://www.roblox.com/item-thumbnails?params=%5B%7BassetId:'+game_id+'%7D%5D'
        game_info = request(url=url)
        game_name = game_info[0]['name']
        game_thumbnail = game_info[0]['thumbnailUrl']
        game_url = game_info[0]['url']

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

        gamejoinleaves: list = [line for line in data.split('\n') if '[FLog::GameJoinLoadTime]' in line or '[FLog::SingleSurfaceApp] handleGameWillClose' in line]
        if not gamejoinleaves:  # Player is not in-game
            return None

        first_join = True
        for item in gamejoinleaves:
            if '[FLog::SingleSurfaceApp] handleGameWillClose' in item:
                first_join = False
        if not first_join:
            i = len(gamejoinleaves) - 1
            while True:
                if i < 0:
                    return None

                if '[FLog::SingleSurfaceApp] handleGameWillClose' in gamejoinleaves[i]:
                    pattern = pattern = r'placeid:(\d+)'
                    match = re.search(pattern, gamejoinleaves[i + 1])
                    if not match:
                        return None

                    game_id = match.group(1)
                    return ['in_game', game_id]

                i = i - 1

        else:  # if first_join:
            pattern = pattern = r'placeid:(\d+)'
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