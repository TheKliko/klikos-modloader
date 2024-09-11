import copy
import time

from modules.other.project import Project
from modules.utils import variables

from .presence import RichPresence
from .server_notification import Notification
from . import log_reader
from . import log_reader_studio


def start(binary_type: str = 'WindowsPlayer') -> None:
    discord_rpc: bool = variables.get('discord_rpc', {}).get('value', False)
    server_notifications: bool = variables.get('server_notifications', {}).get('value', False)

    COOLDOWN: int = 1

    if discord_rpc == False and server_notifications == False:
        return
    
    if discord_rpc == True:
        presence = RichPresence()
        presence.start()
        pass

    if server_notifications == True:
        notification = Notification()

    # Main loop
    activity_watcher = log_reader_studio.ActivityWatcher() if binary_type == 'WindowsStudio' else log_reader.ActivityWatcher()
    old_data: dict = {}
    old_rpc_data: dict = {}
    while True:
        data: dict = activity_watcher.get_data()

        if data == old_data:
            time.sleep(COOLDOWN)
            continue
        old_data = copy.deepcopy(data)

        if data.get('stop', False) == True:
            break

        notification_data: dict = data.get('notification', {})
        if server_notifications == True and notification_data.get('send', False) == True:
            notification.send(
                title=notification_data.get('title', Project.NAME),
                message=notification_data.get('content', 'MESSAGE_FAILED_TO_LOAD')
            )

        rpc_data: dict = data.get('rpc', {})
        if discord_rpc == True and (rpc_data != old_rpc_data or variables.get('do_rpc_update', False) == True):
            old_rpc_data = copy.deepcopy(rpc_data)
            presence.update(
                details=rpc_data.get('details', None),
                state=rpc_data.get('state', None),
                large_image=rpc_data.get('large_image', None),
                large_text=rpc_data.get('large_text', None),
                small_image=rpc_data.get('small_image', None),
                small_text=rpc_data.get('small_text', None),
                start=rpc_data.get('start', None),
                end=rpc_data.get('end', None),
                buttons=rpc_data.get('buttons', None)
            )

        time.sleep(COOLDOWN)