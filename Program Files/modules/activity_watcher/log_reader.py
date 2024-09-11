import copy
import glob
import json
import os
import time

from modules.other.api import RobloxApi, Api
from modules.other.paths import Directory
from modules.other.project import Project
from modules.utils import request
from modules.utils import variables

from .presence_default import DefaultRPC


class OldLogFile:
    prefix: str = r'[FLog::SingleSurfaceApp]'
    startswith: str = r'unregisterMemoryPrioritizationCallback'
class GameJoining:
    prefix: str = r'[FLog::SingleSurfaceApp]'
    startswith: str = r'launchUGCGameInternal'

class GameJoin:
    prefix: str = r'[FLog::GameJoinUtil]'
    startswith: str = r'Game join succeeded.'

class GameTeleport:
    prefix: str = r'[FLog::SingleSurfaceApp]'
    startswith: str = r'initiateTeleport'

class GamePrivateServer:
    prefix: str = r'[FLog::GameJoinUtil]'
    startswith: str = r'GameJoinUtil::joinGamePostPrivateServer'

class GameReservedServer:
    prefix: str = r'[FLog::GameJoinUtil]'
    startswith: str = r'GameJoinUtil::initiateTeleportToReservedServer'

class GameServerId:
    prefix: str = r'[FLog::Network]'
    startswith: str = r'serverId: '

class GameData:
    prefix: str = r'[FLog::Output]'
    startswith: str = r'! Joining game'

class BloxstrapRPC:
    prefix: str = r'[FLog::Output]'
    startswith: str = r'[BloxstrapRPC] '

class GameLeave:
    prefix: str = r'[FLog::SingleSurfaceApp]'
    startswith: str = r'handleGameWillClose'


class Log:
    def __init__(self, prefix: str, data: str):
        self.prefix = prefix
        self.data = data


class ActivityWatcher:
    activity_default: dict = {
        'roblox_open': False,
        'is_playing': False,
        'timestamp': None,
        'game': {
            'server_id': None,
            'location': {
                'city': None,
                'country': None
            },
            'job_id': None,
            'place_id': None,
            'root_place_id': None,
            'universe_id': None,
            'name': None,
            'creator': None,
            'thumbnail': None,
            'is_private_server': False,
            'is_reserved_server': False
        },
        'bloxstrap_rpc': False,
        'bloxstrap_rpc_data': {},
        'send_notification': False,
        'notification_title': None,
        'notification_message': None,
        'stop_activity_watcher': False
    }
    roblox_open: bool = False
    bloxstrap_sdk: bool = False


    def __init__(self) -> None:
        self.log_directory: str = os.path.join(Directory.ROBLOX_LOCALAPPDATA, 'Logs')
        self.activity_data: dict = copy.deepcopy(self.activity_default)
        self.bloxstrap_sdk = variables.get('bloxstrap_sdk', {}).get('value', False)


    def _read_logs(self) -> list[Log]:
        latest_log: str = max(glob.glob(f'{self.log_directory}/*.log'), key=os.path.getmtime)
        with open(latest_log, 'r', encoding='utf-8', errors='replace') as log:
            data = [line.strip() for line in log.readlines()]
            log.close()
        
            logs: list = []
            for entry in data:
                try:
                    prefix: str = entry.split(' ')[1]
                    data: str = ' '.join(entry.split(' ')[2:])
                    log: Log = Log(prefix, data)
                    logs.append(log)
                except IndexError:
                    continue

        return logs
    

    def _is_old_log(self, logs) -> bool:
        last_entry: Log = logs[-1]
        return last_entry.prefix == OldLogFile.prefix and last_entry.data.startswith(OldLogFile.startswith)
    

    def _update(self) -> None:
        logs: list[Log] = self._read_logs()
        if self._is_old_log(logs) and self.activity_data.get('roblox_open', False) == True:
            self.activity_data = copy.deepcopy(self.activity_default)
            self.activity_data['stop_activity_watcher'] = True
            return
        
        self.activity_data['roblox_open'] = True

        # Some default values
        self.activity_data['bloxstrap_rpc'] = self.activity_default['bloxstrap_rpc']
        self.activity_data['bloxstrap_rpc_data'] = self.activity_default['bloxstrap_rpc_data']
        self.activity_data['game']['is_private_server'] = self.activity_default['game']['is_private_server']
        self.activity_data['game']['is_reserved_server'] = self.activity_default['game']['is_reserved_server']
        self.activity_data['send_notification'] = self.activity_default['send_notification']
        self.activity_data['notification_title'] = self.activity_default['notification_title']
        self.activity_data['notification_message'] = self.activity_default['notification_message']

        for log in reversed(logs):
            is_game_leave: bool = log.prefix == GameLeave.prefix and log.data.startswith(GameLeave.startswith)
            is_bloxstrap_rpc: bool = log.prefix == BloxstrapRPC.prefix and log.data.startswith(BloxstrapRPC.startswith)
            is_game_joining: bool = log.prefix == GameJoining.prefix and log.data.startswith(GameJoining.startswith)
            is_game_teleport: bool = log.prefix == GameTeleport.prefix and log.data.startswith(GameTeleport.startswith)

            # User leaves a game
            if is_game_leave:
                self.activity_data = copy.deepcopy(self.activity_default)
                self.activity_data['roblox_open'] = True
                break

            # BloxstrapRPC
            elif is_bloxstrap_rpc:
                self.activity_data['bloxstrap_rpc'] = True
            
                bloxstrap_rpc_log_entry: dict = json.loads(log.data.removeprefix(BloxstrapRPC.startswith))
                command: str = bloxstrap_rpc_log_entry.get('command', None)
                data: dict = bloxstrap_rpc_log_entry.get('data', None)

                # Ignore BloxstrapRPC if data is missing or if command != 'SetRichPresence'
                if not data or command != 'SetRichPresence':
                    continue

                if command == 'SetRichPresence':
                    for key in data.keys():
                        self.activity_data['bloxstrap_rpc_data'][key] = data[key]
                break
        
            # User joins a game, or is teleported
            elif is_game_joining or is_game_teleport:
                user_in_game: bool = False

                if self.activity_data['timestamp'] == None:
                    self.activity_data['timestamp'] = str(int(time.time()))

                game_data: dict= self.activity_default['game']
                location_data: dict = game_data['location']
                server_id = None
                city = None
                country = None
                job_id = None
                place_id = None
                universe_id = None

                # Extract game info from logs
                game_join_logs = logs[logs.index(log):]
                for log in game_join_logs:
                    is_game_joined: bool = log.prefix == GameJoin.prefix and log.data.startswith(GameJoin.startswith)
                    is_private_server: bool = log.prefix == GamePrivateServer.prefix and log.data.startswith(GamePrivateServer.startswith)
                    is_reserved_server: bool = log.prefix == GameReservedServer.prefix and log.data.startswith(GameReservedServer.startswith)

                    # Check if user joined the game
                    if is_game_joined == True:
                        user_in_game = True
                    
                    # Check for private servers
                    elif is_private_server == True:
                        self.activity_data['game']['is_private_server'] = True
                        game_data['is_private_server'] = True

                    # Check for reserved server
                    elif is_reserved_server == True:
                        self.activity_data['game']['is_reserbed_server'] = True
                        game_data['is_reserved_server'] = True

                    # Get server IP adress
                    elif log.prefix == GameServerId.prefix and log.data.startswith(GameServerId.startswith):
                        server_id: str = log.data.removeprefix(GameServerId.startswith).split('|')[0]
                    
                    # Get game data (job_id, place_id)
                    elif log.prefix == GameData.prefix and log.data.startswith(GameData.startswith):
                        log_data: list = log.data.split(' ')
                        for i, data in enumerate(log_data):
                            if log_data[i-1] == 'game':
                                job_id = data.removeprefix('\'').removesuffix('\'')
                            elif log_data[i-1] == 'place':
                                place_id = data
                
                if self.activity_data['is_playing'] == True and not is_game_teleport:
                    break

                # In case log data is read after the GameJoin entry, but before the other entries
                if server_id == None or user_in_game == False:
                    break

                # Safety measure to prevent unnecesary updates
                if job_id == self.activity_data['game']['job_id']:
                    break

                # Get universe id
                url: str = RobloxApi.game_universe_id(place_id)
                response = request.get(url)
                response.raise_for_status()
                data: dict = response.json()
                universe_id: str = data['universeId']

                # Get game info
                url: str = RobloxApi.game_info(universe_id)
                response = request.get(url)
                response.raise_for_status()
                data: dict = response.json()
                root_place_id: str = data['data'][0]['rootPlaceId']
                name: str = data['data'][0]['name']
                creator: str = data['data'][0]['creator']['name']

                # Get game thumbnail
                url: str = RobloxApi.game_thumbnail(universe_id)
                response = request.get(url)
                response.raise_for_status()
                data: dict = response.json()
                thumbnail: str = data['data'][0]['imageUrl']

                # Get location data using ipinfo
                url: str = Api.ip_info(server_id)
                response = request.get(url)
                response.raise_for_status()
                data: dict = response.json()
                city: str = data.get('city', 'ERROR')
                country: str = data.get('country', 'ERROR')
                location_data['city'] = city
                location_data['country'] = country

                # Convert country code to country name,
                if country != 'ERROR':
                    url: str = Api.country_name(country)
                    response = request.get(url)
                    response.raise_for_status()
                    data: dict = response.json()
                    try:
                        country = data[0]['name']['common']
                    except:
                        pass
                    location_data['country'] = country

                # Add data to game_data
                game_data['server_id'] = server_id
                game_data['job_id'] = job_id
                game_data['place_id'] = place_id
                game_data['universe_id'] = universe_id
                game_data['root_place_id'] = root_place_id
                game_data['name'] = name
                game_data['creator'] = creator
                game_data['thumbnail'] = thumbnail
                game_data['location'] = location_data

                self.activity_data['game'] = game_data
                self.activity_data['is_playing'] = True

                self.activity_data['send_notification'] = True
                self.activity_data['notification_title'] = 'Server Joined!'
                self.activity_data['notification_message'] = f'IP Adress: {server_id}\nLocation: {city}, {country}'

                break
    

    def _extract_rpc_data(self, activity_data: dict) -> dict:
        data: dict = {
                'details': DefaultRPC.ROBLOX_PLAYER_DETAILS,
                'state': DefaultRPC.STATE,
                'large_image': DefaultRPC.ROBLOX_PLAYER_LARGE_IMAGE,
                'large_text': DefaultRPC.ROBLOX_PLAYER_LARGE_TEXT,
                'small_image': DefaultRPC.SMALL_IMAGE,
                'small_text': DefaultRPC.SMALL_TEXT,
                'start': None,
                'end': None,
                'buttons': None
            }
        game_data: dict = activity_data.get('game', {})

        data['details'] = f'Playing {game_data.get('name', 'ERROR_BAD_DATA')}'
        data['state'] = f'By {game_data.get('creator', 'ERROR_BAD_DATA')}'
        data['large_image'] = game_data.get('thumbnail', DefaultRPC.ROBLOX_PLAYER_LARGE_IMAGE)
        data['large_text'] = game_data.get('name', DefaultRPC.ROBLOX_PLAYER_LARGE_TEXT)
        data['small_image'] = DefaultRPC.ROBLOX_PLAYER_LARGE_IMAGE
        data['small_text'] = DefaultRPC.ROBLOX_PLAYER_LARGE_TEXT
        data['start'] = activity_data.get('timestamp', None)

        activity_joining: bool = variables.get('activity_joining', {}).get('value', False)
        root_place_id: str = game_data.get('root_place_id', None)
        job_id: str = game_data.get('job_id', None)
        
        if root_place_id == None:
            return data
        
        buttons: list[dict[str,str]] = [
            {'label':'View Game Page', 'url': rf'https://www.roblox.com/games/{root_place_id}/'}
        ]
        if activity_joining == True and job_id != None:
            buttons.append(
                {'label':'Join Server', 'url': rf'roblox://experiences/start?placeId={game_data['root_place_id']}&gameInstanceId={game_data['job_id']}/'}
            )
        data['buttons'] = buttons

        return data
    

    def get_data(self) -> dict:
        data: dict = {
            'notification': {
                'send': False,
                'title': Project.NAME,
                'content': None
            },
            'rpc': {
                'details': DefaultRPC.ROBLOX_PLAYER_DETAILS,
                'state': DefaultRPC.STATE,
                'large_image': DefaultRPC.ROBLOX_PLAYER_LARGE_IMAGE,
                'large_text': DefaultRPC.ROBLOX_PLAYER_LARGE_TEXT,
                'small_image': DefaultRPC.SMALL_IMAGE,
                'small_text': DefaultRPC.SMALL_TEXT,
                'start': None,
                'end': None,
                'buttons': None
            },
            'stop': False
        }
        self._update()
        activity_data: dict = self.activity_data

        if (activity_data.get('roblox_open', False) == False and self.roblox_open == True) or activity_data.get('stop_activity_watcher', False) == True:
            data['stop'] = True
            return data
        elif activity_data.get('roblox_open', False) == False:
            self.roblox_open = True
        
        if activity_data.get('is_playing', False) == False:
            return data

        if activity_data.get('send_notification', False) == True:
            data['notification']['send'] = True
            data['notification']['title'] = activity_data.get('notification_title', Project.NAME)
            data['notification']['content'] = activity_data.get('notification_message', 'MESSAGE_FAILED_TO_LOAD')
        
        if activity_data.get('is_playing', False) == True:
            data['rpc'] = self._extract_rpc_data(activity_data)

            if activity_data.get('bloxstrap_rpc', False) == True:
                bloxstrap_rpc_data: dict = activity_data.get('bloxstrap_rpc_data', None)

                if bloxstrap_rpc_data == None or bloxstrap_rpc_data.get('') or self.bloxstrap_sdk == False:
                    return data
                
                data['rpc']['details'] = bloxstrap_rpc_data.get('details', None)
                data['rpc']['state'] = bloxstrap_rpc_data.get('state', None)

                start = bloxstrap_rpc_data.get('timeStart', None)
                end = bloxstrap_rpc_data.get('timeEnd', None)
                if start == 0:
                    start = None
                if end == 0:
                    end = None
                data['rpc']['start'] = start
                data['rpc']['end'] = end
                
                large_image_data: dict = bloxstrap_rpc_data.get('largeImage', None)
                small_image_data: dict = bloxstrap_rpc_data.get('smallImage', None)
                if large_image_data != None:
                    if large_image_data.get('clear', False) == True or large_image_data.get('assetId', None) == None:
                        data['rpc']['large_image'] = None
                        data['rpc']['large_text'] = None
                    elif large_image_data.get('reset', False) == True:
                        pass
                    elif large_image_data.get('assetId', None) != None:
                        data['rpc']['large_image'] = rf'https://assetdelivery.roblox.com/v1/asset/?id={large_image_data['assetId']}'
                        data['rpc']['large_text'] = large_image_data.get('hoverText', data['rpc']['large_text'])
                
                    if small_image_data.get('clear', False) == True or small_image_data.get('assetId', None) == None:
                        data['rpc']['small_image'] = None
                        data['rpc']['small_text'] = None
                    elif small_image_data.get('reset', False) == True:
                        pass
                    elif small_image_data.get('assetId', None) != None:
                        data['rpc']['small_image'] = rf'https://assetdelivery.roblox.com/v1/asset/?id={small_image_data['assetId']}'
                        data['rpc']['small_text'] = small_image_data.get('hoverText', data['rpc']['small_text'])

        return data