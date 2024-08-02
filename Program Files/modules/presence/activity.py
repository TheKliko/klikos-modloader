import glob
import os
import re
import time

from modules.presence.status import RichPresenceStatus
from modules.utils import variables
from modules.utils.request import request, RequestType


GAME_JOIN: str = '[FLog::GameJoinUtil] Game join succeeded'
GAME_JOIN_DATA: str = '[FLog::GameJoinLoadTime]'
GAME_LEAVE: str = '[FLog::SingleSurfaceApp] handleGameWillClose'
ROBLOX_PLAYER_CLOSED: str = '[FLog::SingleSurfaceApp] unregisterMemoryPrioritizationCallback'

STUDIO_JOIN: str = '[FLog::RobloxIDEDoc] RobloxIDEDoc::open - start'
STUDIO_LEAVE: str = '[FLog::RobloxIDEDoc] RobloxIDEDoc::doClose'
ROBLOX_STUDIO_CLOSED: str = '[FLog::StudioApplicationState] AboutToQuit'

ROBLOX_LOGGING_DIRECTORY: str = os.path.join(os.getenv('LOCALAPPDATA'), 'Roblox', 'Logs')


def update() -> str | None:
    """Update rpc status"""

    LATEST_LOG: str = max(glob.glob(f'{ROBLOX_LOGGING_DIRECTORY}/*.log'), key=os.path.getmtime)
    with open(LATEST_LOG, 'r') as file:
        data = file.read()
        file.close()

    for line in reversed(data.splitlines()):
        if GAME_JOIN_DATA in line:
            variables.set('gamejoindata', line)

        if ROBLOX_PLAYER_CLOSED in line or ROBLOX_STUDIO_CLOSED in line:
            return None
        
        elif GAME_LEAVE in line:
            return RichPresenceStatus.ROBLOX

        elif STUDIO_LEAVE in line:
            variables.remove('rpc_timestamp')
            return RichPresenceStatus.STUDIO

        elif GAME_JOIN in line:
            gamejoindata: str = variables.get('gamejoindata')

            pattern: str = r'universeid:(?P<universeid>\d+).*?clienttime:(?P<clienttime>\d+\.\d+)'
            match = re.search(pattern, gamejoindata)

            universe_id: str = match.group('universeid')

            GAME_INFO_URL: str = rf'https://games.roblox.com/v1/games?universeIds={universe_id}'
            GAME_THUMBNAIL_URL: str = rf'https://thumbnails.roblox.com/v1/games/icons?universeIds={universe_id}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false'

            name: str = request(GAME_INFO_URL)['data'][0]['name']
            image: str = request(GAME_THUMBNAIL_URL)['data'][0]['imageUrl']
            timestamp: str = match.group('clienttime')

            variables.set('rpc_name', name)
            variables.set('rpc_image', image)
            variables.set('rpc_timestamp', int(float(timestamp)))

            variables.remove('gamejoindata')
            return RichPresenceStatus.PLAYING

        elif STUDIO_JOIN in line:
            pattern: str = r'placeId:\s*(\d+)'
            match = re.search(pattern, line)

            place_id: str = match.group(1)

            UNIVERSE_ID_URL: str = rf'https://apis.roblox.com/universes/v1/places/{place_id}/universe'
            universe_id: str = request(UNIVERSE_ID_URL, RequestType.JSON_VALUE, 'universeId')

            GAME_INFO_URL: str = rf'https://games.roblox.com/v1/games?universeIds={universe_id}'
            GAME_THUMBNAIL_URL: str = rf'https://thumbnails.roblox.com/v1/games/icons?universeIds={universe_id}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false'

            name: str = request(GAME_INFO_URL)['data'][0]['name']
            image: str = request(GAME_THUMBNAIL_URL)['data'][0]['imageUrl']

            if not variables.get('rpc_timestamp'):
                timestamp: str = int(time.time())
                variables.set('rpc_timestamp', timestamp)

            variables.set('rpc_name', name)
            variables.set('rpc_image', image)

            variables.remove('gamejoindata')
            return RichPresenceStatus.CREATING
    return None


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()