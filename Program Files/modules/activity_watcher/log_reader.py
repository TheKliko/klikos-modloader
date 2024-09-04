import os

from modules.other.paths import Directory


class ActivityWatcher:
    rpc_default: dict = {
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
        'user_channel': None,
        'stop_activity_watcher': False
    }

    def __init__(self) -> None:
        self.log_directory: str = os.path.join(Directory.ROBLOX_LOCALAPPDATA, 'Logs')