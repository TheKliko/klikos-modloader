from copy import deepcopy
import threading
import time
import glob
import os
import logging
import re
import json
import sys

from modules import request
from modules.request import RobloxApi
from modules.info import Project
from modules.filesystem import Directory

from cooldown import COOLDOWN
from .log_data import StudioLogData as LogData


class Entry:
    def __init__(self, prefix: str, data: str) -> None:
        self.prefix = prefix
        self.data = data


class StudioActivityWatcher:
    log_directory: str = Directory.roblox_logs()

    roblox_open: bool = False
    is_creating: bool = False
    pause_data_update: bool = False
    default_data: dict = {
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
        "bloxstrap_rpc_data": {}
    }
    activity_data: dict = deepcopy(default_data)
    old_activity_data: dict = deepcopy(default_data)

    rpc_data_default: dict = {
        "details": "Playing Roblox Studio . . .",
        "state": None,
        "start": None,
        "end": None,
        "buttons": None,
        "large_image": "studio",
        "large_text": "Roblox Studio",
        "small_image": "modloader",
        "small_text": Project.NAME
    }
    rpc_data: dict = deepcopy(rpc_data_default)

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
            try:
                time.sleep(COOLDOWN)
                logs: list[Entry] = self._log_reader()
                old_log_file: bool = self._is_old_log(logs)

                if old_log_file and self.roblox_open:
                    self._stop_event.set()
                elif old_log_file:
                    continue
                self.roblox_open = True

                self._set_activity_data(logs)

                if self.pause_data_update:
                    self.pause_data_update = False
                    continue

                if self.is_creating:
                    self._set_rpc_data()
                else:
                    self.rpc_data = deepcopy(self.rpc_data_default)

            except Exception as e:
                logging.error(type(e).__name__+": "+str(e))
                logging.info("Continuing in 5 seconds . . .")
                time.sleep(5)
    

    def _log_reader(self) -> list[Entry]:
        latest_log: str = max([item for item in glob.glob(f"{self.log_directory}/*.log") if "studio" in item.lower()], key=os.path.getmtime)
        logs: list[Entry] = []
        with open(latest_log, "r", encoding="utf-8", errors="replace") as file:
            log_data = [line.strip() for line in file.readlines()]
            file.close()
        
            for entry in log_data:
                try:
                    prefix: str = entry.split(" ")[1]
                    data: str = " ".join(entry.split(" ")[2:])
                    log: Entry = Entry(prefix, data)
                    logs.append(log)

                except IndexError:
                    continue
        return logs


    def _is_old_log(self, logs: list[Entry]) -> bool:
        entry: Entry = logs[-1]
        return entry.prefix == LogData.OldLogFile.prefix and entry.data.startswith(LogData.OldLogFile.startswith)


    def _set_activity_data(self, logs: list[Entry]) -> None:
        self.activity_data = deepcopy(self.default_data)
        self.bloxstrap_rpc = False
        for entry in reversed(logs):
            is_game_leave: bool = entry.prefix == LogData.GameLeave.prefix and entry.data.startswith(LogData.GameLeave.startswith)
            is_bloxstrap_rpc: bool = entry.prefix == LogData.BloxstrapRPC.prefix and entry.data.startswith(LogData.BloxstrapRPC.startswith)
            is_game_join: bool = entry.prefix == LogData.GameJoin.prefix and entry.data.startswith(LogData.GameJoin.startswith)

            if is_game_leave:
                self.is_creating = False
                self.old_activity_data = deepcopy(self.default_data)
                return
            
            elif is_bloxstrap_rpc:
                bloxstrap_rpc_data: dict = json.loads(entry.data.removeprefix(LogData.BloxstrapRPC.startswith))
                bloxstrap_rpc_command: str = bloxstrap_rpc_data.get("command", None)
                bloxstrap_rpc_data: dict = bloxstrap_rpc_data.get("data", None)
                if bloxstrap_rpc_command != "SetRichPresence" or not bloxstrap_rpc_data:
                    continue

                self.activity_data = deepcopy(self.old_activity_data)

                self.bloxstrap_rpc = True
                for key in bloxstrap_rpc_data.keys():
                    self.activity_data["bloxstrap_rpc"][key] = bloxstrap_rpc_data[key]
                return
            
            elif is_game_join:
                if self.is_creating:
                    self.pause_data_update = True
                    return
                
                line: str = entry.prefix+" "+entry.data
                pattern: str = r'placeId:\s*(\d+)'
                match = re.search(pattern, line)
                place_id: str = match.group(1)

                if not place_id:
                    self.pause_data_update = True
                    return
                
                universe_id = self._set_universe_id(place_id)
                self._set_game_info(universe_id)
                self._set_thumbnail(universe_id)

                self.activity_data["timestamp"] = str(int(time.time()))
                self.old_activity_data = deepcopy(self.activity_data)
                self.is_creating = True
                return
        
    
    def _set_universe_id(self, place_id: str) -> str:
        response = request.get(RobloxApi.game_universe_id(place_id))
        data: dict = response.json()
        universe_id: str = str(data["universeId"])
        self.activity_data["game"]["universe_id"] = universe_id
        return universe_id
    

    def _set_game_info(self, universe_id: str) -> None:
        url: str = RobloxApi.game_info(universe_id)
        response = request.get(url)
        response.raise_for_status()
        data: dict = response.json()
        root_place_id: str = str(data["data"][0]["rootPlaceId"])
        name: str = str(data["data"][0]["name"])
        creator: str = str(data["data"][0]["creator"]["name"])

        self.activity_data["game"]["root_place_id"] = root_place_id
        self.activity_data["game"]["name"] = name
        self.activity_data["game"]["creator"] = creator


    def _set_thumbnail(self, universe_id: str) -> None:
        url: str = RobloxApi.game_thumbnail(universe_id)
        response = request.get(url)
        response.raise_for_status()
        data: dict = response.json()
        thumbnail: str = str(data["data"][0]["imageUrl"])
        self.activity_data["game"]["thumbnail"] = thumbnail


    def _set_rpc_data(self) -> None:
        if not self.is_creating:
            self.rpc_data = deepcopy(self.rpc_data_default)
        
        game_data: dict = self.activity_data["game"]
        root_place_id: str = game_data["root_place_id"]

        buttons: list[dict[str,str]] = [
            {"label": "View on Roblox", "url": RobloxApi.game_page(root_place_id)}
        ]

        details = "Editing "+str(game_data["name"])
        state = "By "+str(game_data["creator"])
        large_image = game_data["thumbnail"]
        large_text = game_data["name"]
        small_image = "studio"
        small_text = "Roblox Studio"
        start = self.activity_data["timestamp"]
        end = None

        if self.bloxstrap_rpc:
            bloxstrap_rpc_data = self.activity_data["bloxstrap_rpc"]

            start = bloxstrap_rpc_data.get("timeStart", start) if bloxstrap_rpc_data.get("timeStart", start) != 0 else start
            end = bloxstrap_rpc_data.get("timeEnd", end) if bloxstrap_rpc_data.get("timeEnd", start) != 0 else start
            bloxstrap_rpc_data.get("details", details)
            bloxstrap_rpc_data.get("state", state)

            large_image_data: dict = bloxstrap_rpc_data.get("largeImage", None)
            small_image_data: dict = bloxstrap_rpc_data.get("smallImage", None)
            if large_image_data:
                if large_image_data.get("clear", False) == True or large_image_data.get("assetId", None) is None:
                    large_image = None
                    large_text = None
                elif large_image_data.get("reset", False) == True:
                    pass
                elif large_image_data.get("assetId", None) is not None:
                    large_image = RobloxApi.game_asset(large_image_data["assetId"])
                    large_text = large_image_data.get("hoverText", large_text)

            if small_image_data:
                if small_image_data.get("clear", False) == True or small_image_data.get("assetId", None) is None:
                    small_image = None
                    small_text = None
                elif small_image_data.get("reset", False) == True:
                    pass
                elif small_image_data.get("assetId", None) is not None:
                    small_image = RobloxApi.game_asset(small_image_data["assetId"])
                    small_text = small_image_data.get("hoverText", small_text)

        self.rpc_data = {
            "details": details,
            "state": state,
            "start": start,
            "end": end,
            "buttons": buttons,
            "large_image": large_image,
            "large_text": large_text,
            "small_image": small_image,
            "small_text": small_text
        }
    

    def get_data(self) -> dict:
        return self.rpc_data