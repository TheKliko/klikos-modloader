import copy
import time

from modules.other.project import Project
from modules.utils import variables

from .presence import RichPresence
from .server_notification import Notification
from .log_reader import ActivityWatcher
from .presence_default import DefaultRPC


def start() -> None:
    discord_rpc: bool = variables.get('discord_rpc', {}).get('value', False)
    server_notifications: bool = variables.get('server_notifications', {}).get('value', False)
    activity_joining: bool = variables.get('activity_joining', {}).get('value', False)
    bloxstrap_sdk: bool = variables.get('bloxstrap_sdk', {}).get('value', False)

    if discord_rpc == False and server_notifications == False:
        return
    
    if discord_rpc == True:
        presence = RichPresence()
        presence.start()
        pass

    if server_notifications == True:
        notification = Notification()

    # Main loop
    activity_watcher = ActivityWatcher()
    old_data: dict = {}
    while True:
        activity_data: dict = activity_watcher.update()

        if activity_data == None:
            presence.stop()
            break
        if activity_data.get('stop_activity_watcher', False) == True:
            presence.stop()
            break

        if server_notifications == True:
            if activity_data.get('send_notification', False) == True:
                notification.send(
                    title=activity_data.get('notification_title', Project.NAME),
                    message=activity_data.get('notification_message', 'MESSAGE_FAILED_TO_LOAD')
                )
        
        if discord_rpc == True:
            details: str = None
            state: str = None
            large_image: str = None
            large_text: str = None
            small_image: str = None
            small_text: str = None
            start: str = None
            end: str = None
            buttons: list[dict[str, str]] = None
            binary_type: str = variables.get('binary_type', 'WindowsPlayer')
            if binary_type.endswith('Studio'):
                details = DefaultRPC.ROBLOX_STUDIO_DETAILS
                large_image=DefaultRPC.ROBLOX_STUDIO_LARGE_IMAGE
                large_text=DefaultRPC.ROBLOX_STUDIO_LARGE_TEXT
            else:
                details = DefaultRPC.ROBLOX_PLAYER_DETAILS
                large_image=DefaultRPC.ROBLOX_PLAYER_LARGE_IMAGE
                large_text=DefaultRPC.ROBLOX_PLAYER_LARGE_TEXT
            state=DefaultRPC.STATE
            small_image=DefaultRPC.SMALL_IMAGE
            small_text=DefaultRPC.SMALL_TEXT

            is_private_server: bool = False
            is_reserverd_server: bool = False
            if activity_data['is_playing'] == True:
                is_private_server = activity_data['game']['is_private_server']
                is_reserverd_server = activity_data['game']['is_reserved_server']

            if activity_data['is_playing'] == True and (activity_data['bloxstrap_rpc'] == False or bloxstrap_sdk == False):
                details = f'Playing {activity_data['game']['name']}'
                buttons = [
                    {'label':'Visit Game Page', 'url': rf'https://www.roblox.com/games/{activity_data['game']['root_place_id']}/'}
                ]

                if is_private_server == False and is_reserverd_server == False:
                    state = f'By {activity_data['game']['creator']}'
                    if activity_joining == True:
                        buttons = [
                            {'label':'Visit Game Page', 'url': rf'https://www.roblox.com/games/{activity_data['game']['root_place_id']}/'},
                            {'label':'Join Game', 'url': rf'roblox://experiences/start?placeId={activity_data['game']['root_place_id']}&gameInstanceId={activity_data['game']['job_id']}/'}
                        ]

                elif is_private_server == True:
                    state = 'In a private server'

                elif is_reserverd_server == True:
                    state = 'In a reserved server'

                start = activity_data['timestamp']
                large_image = activity_data['game']['thumbnail']
                large_text = activity_data['game']['name']
            
            elif activity_data['is_playing'] == True and activity_data['bloxstrap_rpc'] == True:
                bloxstrap_rpc_data: dict = activity_data['bloxstrap_rpc_data']
                details = bloxstrap_rpc_data.get('details', None)
                state = bloxstrap_rpc_data.get('state', None)

                start = bloxstrap_rpc_data.get('timeStart', None)
                end = bloxstrap_rpc_data.get('timeEnd', None)
                if start == 0:
                    start = None
                if end == 0:
                    end = None

                large_image_data: dict = bloxstrap_rpc_data.get('largeImage', None)
                small_image_data: dict = bloxstrap_rpc_data.get('smallImage', None)
                if not large_image_data:
                    large_image = activity_data['game']['thumbnail']
                elif large_image_data.get('clear',False) == True:
                    large_image = None
                elif large_image_data.get('reset', False) == True or large_image_data.get('assetId', None) == None:
                    large_image = activity_data['game']['thumbnail']
                else:
                    large_image = rf'https://assetdelivery.roblox.com/v1/asset/?id={large_image_data['assetId']}'
                    large_text = large_image_data.get('hoverText', None)
                if not small_image_data:
                    small_image = activity_data['game']['thumbnail']
                elif small_image_data.get('clear',False) == True:
                    small_image = None
                elif small_image_data.get('reset', False) == True or small_image_data.get('assetId', None) == None:
                    small_image = activity_data['game']['thumbnail']
                else:
                    small_image = rf'https://assetdelivery.roblox.com/v1/asset/?id={small_image_data['assetId']}'
                    small_text = small_image_data.get('hoverText', None)
                
                if is_private_server == False and is_reserverd_server == False:
                    if activity_joining == True:
                        buttons = [
                            {'label':'Visit Game Page', 'url': rf'https://www.roblox.com/games/{activity_data['game']['root_place_id']}/'},
                            {'label':'Join Game', 'url': rf'roblox://experiences/start?placeId={activity_data['game']['root_place_id']}&gameInstanceId={activity_data['game']['job_id']}/'}
                        ]

                elif is_private_server == True:
                    state = 'In a private server'

                elif is_reserverd_server == True:
                    state = 'In a reserved server'
            
            current_data: dict = {
                'details': details,
                'state': state,
                'large_image': large_image,
                'large_text': large_text,
                'small_image': small_image,
                'small_text': small_text,
                'start': start,
                'end': end,
                'buttons': buttons
            }

            if current_data != old_data:
                presence.update(
                    details=details,
                    state=state,
                    large_image=large_image,
                    large_text=large_text,
                    small_image=small_image,
                    small_text=small_text,
                    start=start,
                    end=end,
                    buttons=buttons
                )
            
            old_data = copy.deepcopy(current_data)

        time.sleep(1)
