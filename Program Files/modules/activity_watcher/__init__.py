import threading

from modules.utils import variables

from .presence import Presence
from .server_notification import Notification
from .log_reader import update_status


def start() -> None:
    discord_rpc: bool = variables.get('discord_rpc', {}).get('value', False)
    server_notification: bool = variables.get('server_notification', {}).get('value', False)

    if discord_rpc == False and server_notification == False:
        return
    

    if discord_rpc == True:
        presence = Presence()
        presence.start()



    raise NotImplementedError('activity_watcher not implemented!')