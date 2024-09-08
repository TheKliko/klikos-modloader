import copy
import glob
import json
import os
import re
import time

from modules.other.api import RobloxApi, Api
from modules.other.paths import Directory
from modules.other.project import Project
from modules.utils import request
from modules.utils import variables

from .presence_default import DefaultRPC


class OldLogFile:
    prefix: str = r'[FLog::StudioApplicationState]'
    startswith: str = r'AboutToQuit'

class StudioGameJoin:
    prefix: str = r'[FLog::RobloxIDEDoc]'
    startswith: str = r'RobloxIDEDoc::open - start'

class BloxstrapRPC:
    prefix: str = r'[FLog::Output]'
    startswith: str = r'[BloxstrapRPC] '

class StudioGameLeave:
    prefix: str = r'[FLog::RobloxIDEDoc]'
    startswith: str = r'RobloxIDEDoc::doClose'


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
        'stop_activity_watcher': False
    }
    studio_open: bool = False
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

        for log in reversed(logs):
            is_game_leave: bool = log.prefix == StudioGameLeave.prefix and log.data.startswith(StudioGameLeave.startswith)
            is_bloxstrap_rpc: bool = log.prefix == BloxstrapRPC.prefix and log.data.startswith(BloxstrapRPC.startswith)
            is_game_join: bool = log.prefix == StudioGameJoin.prefix and log.data.startswith(StudioGameJoin.startswith)

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
        
            # User joins a game
            elif is_game_join:
                if self.activity_data['timestamp'] == None:
                    self.activity_data['timestamp'] = str(int(time.time()))
                
                line: str = f'{log.prefix} {log.data}'

                game_data: dict= self.activity_default['game']
                place_id = None
                universe_id = None
                
                pattern: str = r'placeId:\s*(\d+)'
                match = re.search(pattern, line)
                place_id: str = match.group(1)
                
                if self.activity_data['is_playing'] == True:
                    break
                
                if not place_id:
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

                # Add data to game_data
                game_data['place_id'] = place_id
                game_data['universe_id'] = universe_id
                game_data['root_place_id'] = root_place_id
                game_data['name'] = name
                game_data['creator'] = creator
                game_data['thumbnail'] = thumbnail

                self.activity_data['game'] = game_data
                self.activity_data['is_playing'] = True

                break
    

    def _extract_rpc_data(self, activity_data: dict) -> dict:
        data: dict = {
                'details': DefaultRPC.ROBLOX_STUDIO_DETAILS,
                'state': DefaultRPC.STATE,
                'large_image': DefaultRPC.ROBLOX_STUDIO_LARGE_IMAGE,
                'large_text': DefaultRPC.ROBLOX_STUDIO_LARGE_TEXT,
                'small_image': DefaultRPC.SMALL_IMAGE,
                'small_text': DefaultRPC.SMALL_TEXT,
                'start': None,
                'end': None,
                'buttons': None
            }
        game_data: dict = activity_data.get('game', {})

        data['details'] = f'Playing {game_data.get('name', 'ERROR_BAD_DATA')}'
        data['state'] = f'By {game_data.get('creator'), 'ERROR_BAD_DATA'}'
        data['large_image'] = game_data.get('thumbnail', DefaultRPC.ROBLOX_STUDIO_LARGE_IMAGE)
        data['large_text'] = game_data.get('name', DefaultRPC.ROBLOX_PLAYER_LARGE_TEXT)
        data['small_image'] = DefaultRPC.SMALL_IMAGE
        data['small_text'] = DefaultRPC.SMALL_TEXT
        data['start'] = activity_data.get('timestamp', None)

        root_place_id: str = game_data.get('root_place_id', None)
        
        if root_place_id == None:
            return data
        
        buttons: list[dict[str,str]] = [
            {'label':'View Game Page', 'url': rf'https://www.roblox.com/games/{root_place_id}/'}
        ]
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
                'details': DefaultRPC.ROBLOX_STUDIO_DETAILS,
                'state': DefaultRPC.STATE,
                'large_image': DefaultRPC.ROBLOX_STUDIO_LARGE_IMAGE,
                'large_text': DefaultRPC.ROBLOX_STUDIO_LARGE_TEXT,
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

        if (activity_data.get('roblox_open', False) == False and self.studio_open == True) or activity_data.get('stop_activity_watcher', False) == True:
            data['stop'] = True
            return data
        elif activity_data.get('roblox_open', False) == False:
            self.studio_open = True
        
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