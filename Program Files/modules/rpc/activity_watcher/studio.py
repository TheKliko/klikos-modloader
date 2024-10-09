from copy import deepcopy
import threading
import time

from modules.filesystem import Directory

from ..cooldown import COOLDOWN
from .log_data import StudioLogData as LogData


class Entry:
    def __init__(self, prefix: str, data: str) -> None:
        self.prefix = prefix
        self.data = data


class StudioActivityWatcher:
    stop_rpc: bool = False
    log_directory: str = Directory.roblox_logs()

    default_data: dict = {
        "roblox_open": False,
        "is_playing": False,
        "timestamp": None,
        "game": {
            "place_id": None,
            "root_place_id": None,
            "universe_id": None,
            "name": None,
            "creator": None,
            "thumbnail": None,
            "is_private_server": False,
            "is_reserved_server": False
        },
        "bloxstrap_rpc": False,
        "bloxstrap_rpc_data": {},
        "stop_activity_watcher": False
    }
    activity_data: dict = deepcopy(default_data)
    rpc_data: dict = {}

    _stop_event = threading.Event()


    def __init__(self) -> None:
        if self._stop_event.is_set():
            self._stop_event.clear()

        self.thread = threading.Thread(
            name="activity-watcher-thread",
            target=self._mainloop,
            daemon=True
        )
        self.thread.start()


    def _mainloop(self) -> None:
        while not self._stop_event.is_set():
            

            break

            time.sleep(COOLDOWN)
    
    def get_data(self) -> dict:
        return self.rpc_data