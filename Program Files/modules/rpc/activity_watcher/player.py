from copy import deepcopy
import threading
import time
import glob
import os
import sys
import json
import logging

from modules.info import Project
from modules import request
from modules.request import RobloxApi
from modules.filesystem import Directory
from modules.functions import integrations

from cooldown import COOLDOWN
from .log_data import LogData


class Entry:
    def __init__(self, prefix: str, data: str) -> None:
        self.prefix = prefix
        self.data = data


class ActivityWatcher:
    log_directory: str = Directory.roblox_logs()
    activity_joining: bool = integrations.value("activity_joining", False)

    roblox_open: bool = False
    is_playing: bool = False
    bloxstrap_rpc: bool = False
    pause_data_update: bool = False
    old_job_id = None
    default_data: dict = {
        "game": {
            "job_id": None,
            "place_id": None,
            "root_place_id": None,
            "universe_id": None,
            "name": None,
            "creator": None,
            "thumbnail": None,
            "private_server": False,
            "reserved_server": False
        },
        "timestamp": None,
        "bloxstrap_rpc": {}
    }
    activity_data: dict = deepcopy(default_data)
    old_activity_data: dict = deepcopy(default_data)

    rpc_data_default: dict = {
        "details": "Playing Roblox . . .",
        "state": None,
        "start": None,
        "end": None,
        "buttons": None,
        "large_image": "player",
        "large_text": "Roblox Player",
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

                if self.is_playing:
                    self._set_rpc_data()
                else:
                    self.rpc_data = deepcopy(self.rpc_data_default)

            except Exception as e:
                logging.error(type(e).__name__+": "+str(e))
                logging.info("Continuing in 5 seconds . . .")
                time.sleep(5)
    

    def _log_reader(self) -> list[Entry]:
        latest_log: str = max([item for item in glob.glob(f"{self.log_directory}/*.log") if "player" in item.lower()], key=os.path.getmtime)
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
            is_game_joining: bool = entry.prefix == LogData.GameJoining.prefix and entry.data.startswith(LogData.GameJoining.startswith)
            is_game_teleport: bool = entry.prefix == LogData.GameTeleport.prefix and entry.data.startswith(LogData.GameTeleport.startswith)

            if is_game_leave:
                self.is_playing = False
                self.old_job_id = None
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
            
            elif is_game_joining or is_game_teleport:
                if self.is_playing and not is_game_teleport:
                    self.pause_data_update = True
                    return
                
                user_in_game: bool = False
                game_join_logs: list[Entry] = logs[logs.index(entry):]
                for game_join_entry in game_join_logs:
                    is_game_joined: bool = game_join_entry.prefix == LogData.GameJoin.prefix and game_join_entry.data.startswith(LogData.GameJoin.startswith)
                    is_private_server: bool = game_join_entry.prefix == LogData.GamePrivateServer.prefix and game_join_entry.data.startswith(LogData.GamePrivateServer.startswith)
                    is_reserved_server: bool = game_join_entry.prefix == LogData.GameReservedServer.prefix and game_join_entry.data.startswith(LogData.GameReservedServer.startswith)

                    if is_game_joined:
                        user_in_game = True
                    
                    elif is_private_server:
                        self.activity_data["game"]["private_server"] = True
                    
                    elif is_reserved_server:
                        self.activity_data["game"]["reserved_server"] = True
                    
                    elif game_join_entry.prefix == LogData.GameData.prefix and game_join_entry.data.startswith(LogData.GameData.startswith):
                        game_join_entry_data: list = game_join_entry.data.split(" ")
                        for i, data in enumerate(game_join_entry_data, -1):
                            if game_join_entry_data[i] == "game":
                                job_id = str(data.removeprefix("\"").removesuffix("\""))
                                self.activity_data["game"]["job_id"] = job_id
                            if game_join_entry_data[i] == "place":
                                place_id = str(data)
                                self.activity_data["game"]["place_id"] = place_id
                
                if not user_in_game:
                    self.pause_data_update = True
                    return
                
                if job_id == self.old_job_id:
                    self.pause_data_update = True
                    return
                self.old_job_id = job_id
                
                universe_id = self._set_universe_id(place_id)
                self._set_game_info(universe_id)
                self._set_thumbnail(universe_id)

                self.activity_data["timestamp"] = str(int(time.time()))
                self.old_activity_data = deepcopy(self.activity_data)
                self.is_playing = True
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
        if not self.is_playing:
            self.rpc_data = deepcopy(self.rpc_data_default)
        
        game_data: dict = self.activity_data["game"]
        root_place_id: str = game_data["root_place_id"]
        job_id: str = game_data["job_id"]

        buttons: list[dict[str,str]] = [
            {"label": "View on Roblox", "url": RobloxApi.game_page(root_place_id)}
        ]
        if self.activity_joining:
            buttons.append(
                {"label": "Join", "url": RobloxApi.game_join(root_place_id, job_id)}
            )

        details = "Playing "+str(game_data["name"])
        state = "By "+str(game_data["creator"])
        large_image = game_data["thumbnail"]
        large_text = game_data["name"]
        small_image = "player"
        small_text = "Roblox Player"
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