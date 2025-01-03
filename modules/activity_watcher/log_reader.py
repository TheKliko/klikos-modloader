import os
import re
from typing import Literal
from pathlib import Path

from modules.config import integrations
from modules.filesystem import Directory
from modules import request
from modules.request import Response, Api

from .entry import Entry
from .log_data import LogData


class LogReader:
    class Status:
        default: bool = False
        playing: bool = False
        user_id: str | None = None
        place_id: str | None = None
        root_place_id: str | None = None
        universe_id: str | None = None
        job_id: str | None = None
        timestamp: float | None = None
        name: str = "???"
        creator: str = "???"
        private_server: bool = False
        reserved_server: bool = False
        bloxstrap_rpc: bool = False

    class AssetKeys:
        DEFAULT: str = "modloader"
        PLAYER: str = "roblox"
        STUDIO: str = "studio"


    data: dict = {}
    mode: Literal["Player", "Studio"]


    def __init__(self, mode: Literal["Player", "Studio"]):
        self.mode = mode
    

    def get_status(self) -> dict | None | Literal["DEFAULT"]:
        log: list[Entry] = self._read_latest_log()

        if self._is_old_log(log):
            return None
        
        self._update_status(log)

        if not self.Status.playing or self.Status.default:
            return "DEFAULT"

        small_image: str | None = self.AssetKeys.STUDIO if self.mode == "Studio" else self.AssetKeys.PLAYER
        small_text: str | None = f"Roblox {self.mode}"

        if self.Status.universe_id is not None:
            response: Response = request.get(Api.Roblox.Activity.thumbnail(self.Status.universe_id), cached=True, dont_log_cached_request=True)
            data: dict = response.json()
            thumbnail: str = str(data["data"][0]["imageUrl"])

            response = request.get(Api.Roblox.Activity.game(self.Status.universe_id), cached=True, dont_log_cached_request=True)
            data = response.json()
            self.Status.root_place_id = str(data["data"][0]["rootPlaceId"])
            self.Status.name = str(data["data"][0]["name"])
            self.Status.creator = str(data["data"][0]["creator"]["name"])

            large_text = self.Status.name
        else:
            thumbnail = self.AssetKeys.STUDIO if self.mode == "Studio" else self.AssetKeys.PLAYER
            large_text = f"Roblox {self.mode}"

            small_image = None
            small_text = None
        
        self.data = {
            "start": self.Status.timestamp,
            "end": None,
            "details": f"{'Editing' if self.mode == 'Studio' else 'Playing'} {self.Status.name}...",
            "state": f"by {self.Status.creator}",
            "large_image": thumbnail,
            "large_text": large_text,
            "small_image": small_image,
            "small_text": small_text,
            "buttons": []
        }

        if self.Status.root_place_id is not None:
            self.data["buttons"].append({
                    "label": "View on Roblox",
                    "url": Api.Roblox.Activity.page(self.Status.root_place_id)
            })

        show_user_profile: bool = integrations.get_value("show_user_profile_in_rpc")
        activity_joining: bool = integrations.get_value("activity_joining")

        if activity_joining and self.Status.job_id is not None and self.Status.root_place_id is not None and not self.Status.reserved_server:
            self.data["buttons"].insert(0, {
                "label": "Join Game",
                "url": Api.Roblox.Activity.deeplink(self.Status.root_place_id, self.Status.job_id)
            })
        
        if self.data["buttons"] == []:
            self.data["buttons"] = None
        
        if show_user_profile and self.Status.user_id is not None:
            response = request.get(Api.Roblox.Activity.user_thumbnail(self.Status.user_id), cached=True, dont_log_cached_request=True)
            data = response.json()
            self.data["small_image"] = str(data["data"][0]["imageUrl"])

            response = request.get(Api.Roblox.Activity.user(self.Status.user_id), cached=True, dont_log_cached_request=True)
            data = response.json()
            user_name: str = str(data['name'])
            display_name: str = str(data['displayName'])
            self.data["small_text"] = display_name if user_name == display_name else f"{display_name} ({user_name})"

        if self.Status.bloxstrap_rpc:
            # TODO: BloxstrapRPC
            pass

        return None


    def _read_latest_log(self) -> list[Entry]:
        log_files: list[Path] = [
            Directory.ROBLOX_LOGS / item.name
            for item in Directory.ROBLOX_LOGS.iterdir()
            if item.is_file() and self.mode in item.name
        ]

        filepath: Path = max(log_files, key=os.path.getmtime)

        log_entry_pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z.*?)(?=\d{4}-\d{2}-\d{2}T|$)'
        with open(filepath, "r", encoding="utf-8") as file:
            content: str = file.read()
        
        entries = re.findall(log_entry_pattern, content, re.DOTALL)
        return [Entry(data) for data in reversed(entries)]


    def _is_old_log(self, log: list[Entry]) -> bool:
        if not log:
            return True

        entry: Entry = log[0]
        match self.mode:
            case "Player":
                return (entry.prefixes[0] == LogData.Player.OldlogFile.prefix and LogData.Player.OldlogFile.keyword in entry.message)
            case "Studio":
                return (entry.prefixes[0] == LogData.Studio.OldLogFile.prefix and LogData.Studio.OldLogFile.keyword in entry.message)
    

    def _update_status(self, log: list[Entry]) -> None:
        self.Status.default = False
        self.Status.private_server = False
        self.Status.bloxstrap_rpc = False
        self.Status.reserved_server = False

        match self.mode:
            case "Player":
                for entry in log:
                    is_game_leave: bool = entry.prefixes[0] == LogData.Player.GameLeave.prefix and LogData.Player.GameLeave.keyword in entry.message
                    is_game_join: bool = entry.prefixes[0] == LogData.Player.GameJoin.prefix and LogData.Player.GameJoin.keyword in entry.message
                    is_game_join_loadtime: bool = entry.prefixes[0] == LogData.Player.GameJoinLoadTime.prefix and LogData.Player.GameJoinLoadTime.keyword in entry.message
                    is_game_private_server: bool = entry.prefixes[0] == LogData.Player.GamePrivateServer.prefix and LogData.Player.GamePrivateServer.keyword in entry.message
                    is_game_reserved_server: bool = entry.prefixes[0] == LogData.Player.GameReservedServer.prefix and LogData.Player.GameReservedServer.keyword in entry.message
                    is_bloxstrap_rpc: bool = entry.prefixes[0] == LogData.Player.BloxstrapRPC.prefix and LogData.Player.BloxstrapRPC.keyword in entry.message


                    if is_game_leave:
                        self.Status.private_server = False
                        self.Status.reserved_server = False
                        self.Status.playing = False
                        return
                    
                    elif is_game_private_server:
                        self.Status.private_server = True
                    
                    elif is_game_reserved_server:
                        self.Status.reserved_server = True

                    elif is_bloxstrap_rpc:
                        pass

                    elif is_game_join_loadtime:
                        from modules import Logger
                        Logger.info("game_join_loadtime")
                        data: dict = dict(
                            item.removesuffix(",").split(":", 1)
                            for item in entry.message.removeprefix("Report game_join_loadtime: ").split()
                        )
                        self.Status.user_id = data["userid"]
                        self.Status.place_id = data["placeid"]
                        self.Status.universe_id = data["universeid"]

                    elif is_game_join:
                        Logger.info("game_join")
                        self.Status.timestamp = entry.timestamp
                        pattern = r"game '([a-f0-9\-]+)' place (\d+)"
                        match = re.search(pattern, entry.message)
                        if match:
                            self.Status.job_id = match.group(1)
                            self.Status.place_id = match.group(2)
                        else:
                            self.Status.job_id = None
                        
                        if self.Status.place_id is not None:
                            response: Response = request.get(Api.Roblox.Activity.universe_id(self.Status.place_id), cached=True, dont_log_cached_request=True)
                            data = response.json()
                            self.Status.universe_id = str(data["universeId"])
                        return
            
            
            case "Studio":
                # TODO: Studio RPC
                for entry in log:
                    is_game_leave: bool = entry.prefixes[0] == LogData.Studio.GameLeave.prefix and LogData.Studio.GameLeave.keyword in entry.message
                    is_game_join: bool = entry.prefixes[0] == LogData.Studio.GameJoin.prefix and LogData.Studio.GameJoin.keyword in entry.message
                    pass
        
        self.Status.default = True