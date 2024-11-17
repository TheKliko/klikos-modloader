import os
import json
from datetime import datetime, timezone
from copy import deepcopy
from typing import Optional, Literal

from modules.logger import logger
from modules import request
from modules.request import RobloxActivityApi, Response
from modules.filesystem import Directory
from modules.functions.config import integrations

from .data import LogData, StudioLogData


class Entry:
    def __init__(self, timestamp: int, prefix: str, data: str) -> None:
        self.timestamp = timestamp
        self.prefix = prefix
        self.data = data


ROBLOX_LOGS_DIRECTORY: str = Directory.roblox_logs()
PLAYER_DEFAULT: dict = {
    "start": None,
    "end": None,
    "details": "Playing Roblox",
    "state": "Browsing...",
    "large_image": "roblox",
    "large_text": "Roblox",
    "small_image": None,
    "small_text": None,
    "buttons": None
}
STUDIO_DEFAULT: dict = {
    "start": None,
    "end": None,
    "details": "Playing Roblox Studio",
    "state": "Idling...",
    "large_image": "studio",
    "large_text": "Roblox Studio",
    "small_image": None,
    "small_text": None,
    "buttons": None
}

last_place_id: Optional[str] = None
last_rpc_data: Optional[dict] = None
last_bloxstrap_rpc_formatted_data: Optional[dict] = None
last_timestamp: Optional[int] = None
last_allow_activity_joining: Optional[bool] = False
last_user_in_private_server: bool = False
last_user_in_reserved_server: bool = False


# region Player
def player() -> Optional[dict]:
    global last_place_id, last_rpc_data, last_bloxstrap_rpc_formatted_data, last_timestamp, last_allow_activity_joining
    allow_activity_joining: Optional[bool] = integrations.value("activity_joining")

    log_file: Optional[list[Entry]] = read_log_file("Player")
    if not log_file:
        return None
    
    if is_old_log_file_player(log_file):
        return None
    
    # if log_file[0].prefix == LogData.OldLogFile.prefix and log_file[0].data.startswith(LogData.OldLogFile.startswith):
    #     return None
    bloxstrap_rpc_formatted_data: Optional[dict] = None
    user_in_private_server: bool = False
    user_in_reserved_server: bool = False
    
    for entry in log_file:
        is_game_join: bool = entry.prefix == LogData.GameJoin.prefix and entry.data.startswith(LogData.GameJoin.startswith)
        is_game_leave: bool = entry.prefix == LogData.GameLeave.prefix and entry.data.startswith(LogData.GameLeave.startswith)
        is_bloxstrap_rpc: bool = entry.prefix == LogData.BloxstrapRPC.prefix and entry.data.startswith(LogData.BloxstrapRPC.startswith)

        is_private_server: bool = entry.prefix == LogData.GameLeave.prefix and entry.data.startswith(LogData.GameLeave.startswith)
        is_reserved_server: bool = entry.prefix == LogData.GameLeave.prefix and entry.data.startswith(LogData.GameLeave.startswith)

        if is_game_leave:
            return deepcopy(PLAYER_DEFAULT)
        
        elif is_private_server:
            user_in_private_server = True
        
        elif is_reserved_server:
            user_in_reserved_server = True
        
        elif is_bloxstrap_rpc:
            try:
                bloxstrap_rpc_data_full: dict = json.loads(entry.data.removeprefix(LogData.BloxstrapRPC.startswith))
                bloxstrap_rpc_command: Optional[str] = bloxstrap_rpc_data_full.get("command")
                bloxstrap_rpc_data: Optional[dict] = bloxstrap_rpc_data_full.get("data")

                if bloxstrap_rpc_command != "SetRichPresence" or not isinstance(bloxstrap_rpc_data, dict):
                    continue

                bloxstrap_rpc_data_start: Optional[int] = bloxstrap_rpc_data.get("timeStart")
                bloxstrap_rpc_data_end: Optional[int] = bloxstrap_rpc_data.get("timeEnd")
                bloxstrap_rpc_data_details: Optional[str] = bloxstrap_rpc_data.get("details")
                bloxstrap_rpc_data_state: Optional[str] = bloxstrap_rpc_data.get("state")

                bloxstrap_rpc_data_large_image: Optional[str] = None
                bloxstrap_rpc_data_large_text: Optional[str] = None
                bloxstrap_rpc_data_small_image: Optional[str] = None
                bloxstrap_rpc_data_small_text: Optional[str] = None
                bloxstrap_rpc_data_buttons: Optional[list[dict]] = None

                large_image_data: Optional[dict] = bloxstrap_rpc_data.get("largeImage")
                small_image_data: Optional[dict] = bloxstrap_rpc_data.get("smallImage")

                if isinstance(large_image_data, dict):
                    if large_image_data.get("clear") == True or large_image_data.get("assetId") is None:
                        bloxstrap_rpc_data_large_image = None
                        bloxstrap_rpc_data_large_text = None
                    elif large_image_data.get("reset") == True:
                        pass
                    elif large_image_data.get("assetId") is not None:
                        bloxstrap_rpc_data_large_image = RobloxActivityApi.game_asset(large_image_data["assetId"])
                        bloxstrap_rpc_data_large_text = large_image_data.get("hoverText")

                if isinstance(small_image_data, dict):
                    if small_image_data.get("clear") == True or small_image_data.get("assetId") is None:
                        bloxstrap_rpc_data_small_image = None
                        bloxstrap_rpc_data_small_text = None
                    elif small_image_data.get("reset") == True:
                        pass
                    elif small_image_data.get("assetId") is not None:
                        bloxstrap_rpc_data_small_image = RobloxActivityApi.game_asset(small_image_data["assetId"])
                        bloxstrap_rpc_data_small_text = small_image_data.get("hoverText")

                bloxstrap_rpc_formatted_data = {
                    "start": bloxstrap_rpc_data_start,
                    "end": bloxstrap_rpc_data_end,
                    "details": bloxstrap_rpc_data_details,
                    "state": bloxstrap_rpc_data_state,
                    "large_image": bloxstrap_rpc_data_large_image,
                    "large_text": bloxstrap_rpc_data_large_text,
                    "small_image": bloxstrap_rpc_data_small_image,
                    "small_text": bloxstrap_rpc_data_small_text,
                    "buttons": bloxstrap_rpc_data_buttons
                }
            
            except Exception:
                continue
        
        elif is_game_join:
            job_id: Optional[str] = None
            place_id: Optional[str] = None
            game_join_data: list[str] = entry.data.split()
            for i, item in enumerate(game_join_data, 1):
                if item == "game":
                    job_id = game_join_data[i].strip("'")
                elif item == "place":
                    place_id = game_join_data[i]
            
            # Prevent flooding the logs with cached requests
            if place_id == last_place_id \
                and bloxstrap_rpc_formatted_data == last_bloxstrap_rpc_formatted_data \
                    and entry.timestamp == last_timestamp \
                        and allow_activity_joining == last_allow_activity_joining \
                            and user_in_private_server == last_user_in_private_server \
                                and user_in_reserved_server == last_user_in_reserved_server:
                return last_rpc_data
            
            if job_id is None:
                logger.error(f"Failed to get job_id from log entry: {entry.prefix} {entry.data}")
            if place_id is None:
                logger.error(f"Failed to get place_id from log entry: {entry.prefix} {entry.data}")
                raise Exception("place_id is None")

            response1: Response = request.get(request.RobloxActivityApi.game_universe_id(place_id), cache=True)
            data1: dict = response1.json()
            universe_id: str = str(data1["universeId"])

            response2: Response = request.get(request.RobloxActivityApi.game_info(universe_id), cache=True)
            data2: dict = response2.json()
            root_place_id: str = str(data2["data"][0]["rootPlaceId"])
            name: str = str(data2["data"][0]["name"])
            creator: str = str(data2["data"][0]["creator"]["name"])

            response3: Response = request.get(request.RobloxActivityApi.game_thumbnail(universe_id), cache=True)
            data3: dict = response3.json()
            thumbnail: str = str(data3["data"][0]["imageUrl"])

            rpc_data: dict = {
                "start": entry.timestamp,
                "end": None,
                "details": f"Playing {name}",
                "state": f"By {creator}",
                "large_image": thumbnail,
                "large_text": name,
                "small_image": PLAYER_DEFAULT["large_image"],
                "small_text": PLAYER_DEFAULT["large_text"],
                "buttons": [
                    {"label": "View on Roblox", "url": RobloxActivityApi.game_page(root_place_id)},
                    {"label": "Join Game", "url": RobloxActivityApi.game_join(root_place_id, job_id)}
                ] if allow_activity_joining is True and job_id is not None else [
                    {"label": "View on Roblox", "url": RobloxActivityApi.game_page(root_place_id)}
                ]
            }

            if user_in_private_server is True:
                rpc_data.update({
                    "state": "In a private server"
                })

            if user_in_reserved_server is True:
                rpc_data.update({
                    "state": "In a reserved server"
                })

            if bloxstrap_rpc_formatted_data is not None:
                rpc_data.update(bloxstrap_rpc_formatted_data)
            
            if user_in_reserved_server is True and allow_activity_joining is True:
                rpc_data.update({
                    "buttons": [
                        {"label": "View on Roblox", "url": RobloxActivityApi.game_page(root_place_id)}
                    ]
                })

            last_bloxstrap_rpc_formatted_data = bloxstrap_rpc_formatted_data
            last_place_id = place_id
            last_rpc_data = rpc_data
            last_timestamp = entry.timestamp
            last_allow_activity_joining = allow_activity_joining
            
            return rpc_data
    
    return deepcopy(PLAYER_DEFAULT)



# region Studio
def studio() -> Optional[dict]:
    global last_place_id, last_rpc_data, last_bloxstrap_rpc_formatted_data, last_timestamp
    log_file: Optional[list[Entry]] = read_log_file("Studio")
    if not log_file:
        return None
    
    if log_file[0].prefix == LogData.OldLogFile.prefix and log_file[0].data.startswith(LogData.OldLogFile.startswith):
        return None

    for entry in log_file:
        is_game_join: bool = entry.prefix == StudioLogData.GameJoin.prefix and entry.data.startswith(StudioLogData.GameJoin.startswith)
        is_game_leave: bool = entry.prefix == StudioLogData.GameLeave.prefix and entry.data.startswith(StudioLogData.GameLeave.startswith)
        is_bloxstrap_rpc: bool = entry.prefix == StudioLogData.BloxstrapRPC.prefix and entry.data.startswith(StudioLogData.BloxstrapRPC.startswith)
        bloxstrap_rpc_formatted_data: Optional[dict] = None

        if is_game_leave:
            return deepcopy(STUDIO_DEFAULT)
        
        elif is_bloxstrap_rpc:
            try:
                bloxstrap_rpc_data_full: dict = json.loads(entry.data.removeprefix(StudioLogData.BloxstrapRPC.startswith))
                bloxstrap_rpc_command: Optional[str] = bloxstrap_rpc_data_full.get("command")
                bloxstrap_rpc_data: Optional[dict] = bloxstrap_rpc_data_full.get("data")

                if bloxstrap_rpc_command != "SetRichPresence" or not isinstance(bloxstrap_rpc_data, dict):
                    continue

                bloxstrap_rpc_data_start: Optional[int] = bloxstrap_rpc_data.get("timeStart")
                bloxstrap_rpc_data_end: Optional[int] = bloxstrap_rpc_data.get("timeEnd")
                bloxstrap_rpc_data_details: Optional[str] = bloxstrap_rpc_data.get("details")
                bloxstrap_rpc_data_state: Optional[str] = bloxstrap_rpc_data.get("state")

                bloxstrap_rpc_data_large_image: Optional[str] = None
                bloxstrap_rpc_data_large_text: Optional[str] = None
                bloxstrap_rpc_data_small_image: Optional[str] = None
                bloxstrap_rpc_data_small_text: Optional[str] = None
                bloxstrap_rpc_data_buttons: Optional[list[dict]] = None

                large_image_data: Optional[dict] = bloxstrap_rpc_data.get("largeImage")
                small_image_data: Optional[dict] = bloxstrap_rpc_data.get("smallImage")

                if isinstance(large_image_data, dict):
                    if large_image_data.get("clear") == True or large_image_data.get("assetId") is None:
                        bloxstrap_rpc_data_large_image = None
                        bloxstrap_rpc_data_large_text = None
                    elif large_image_data.get("reset") == True:
                        pass
                    elif large_image_data.get("assetId") is not None:
                        bloxstrap_rpc_data_large_image = RobloxActivityApi.game_asset(large_image_data["assetId"])
                        bloxstrap_rpc_data_large_text = large_image_data.get("hoverText")

                if isinstance(small_image_data, dict):
                    if small_image_data.get("clear") == True or small_image_data.get("assetId") is None:
                        bloxstrap_rpc_data_small_image = None
                        bloxstrap_rpc_data_small_text = None
                    elif small_image_data.get("reset") == True:
                        pass
                    elif small_image_data.get("assetId") is not None:
                        bloxstrap_rpc_data_small_image = RobloxActivityApi.game_asset(small_image_data["assetId"])
                        bloxstrap_rpc_data_small_text = small_image_data.get("hoverText")

                bloxstrap_rpc_formatted_data = {
                    "start": bloxstrap_rpc_data_start,
                    "end": bloxstrap_rpc_data_end,
                    "details": bloxstrap_rpc_data_details,
                    "state": bloxstrap_rpc_data_state,
                    "large_image": bloxstrap_rpc_data_large_image,
                    "large_text": bloxstrap_rpc_data_large_text,
                    "small_image": bloxstrap_rpc_data_small_image,
                    "small_text": bloxstrap_rpc_data_small_text,
                    "buttons": bloxstrap_rpc_data_buttons
                }
            
            except Exception:
                continue

        elif is_game_join:
            place_id: str = entry.data.rstrip().removeprefix(StudioLogData.GameJoin.startswith).removesuffix(StudioLogData.GameJoin.endswith)
            
            # Prevent flooding the logs with cached requests
            if place_id == last_place_id and bloxstrap_rpc_formatted_data == last_bloxstrap_rpc_formatted_data and entry.timestamp == last_timestamp:
                return last_rpc_data

            response1: Response = request.get(request.RobloxActivityApi.game_universe_id(place_id), cache=True)
            data1: dict = response1.json()
            universe_id: str = str(data1["universeId"])

            response2: Response = request.get(request.RobloxActivityApi.game_info(universe_id), cache=True)
            data2: dict = response2.json()
            root_place_id: str = str(data2["data"][0]["rootPlaceId"])
            name: str = str(data2["data"][0]["name"])
            creator: str = str(data2["data"][0]["creator"]["name"])

            response3: Response = request.get(request.RobloxActivityApi.game_thumbnail(universe_id), cache=True)
            data3: dict = response3.json()
            thumbnail: str = str(data3["data"][0]["imageUrl"])

            rpc_data: dict = {
                "start": entry.timestamp,
                "end": None,
                "details": f"Editing {name}",
                "state": f"By {creator}",
                "large_image": thumbnail,
                "large_text": name,
                "small_image": STUDIO_DEFAULT["large_image"],
                "small_text": STUDIO_DEFAULT["large_text"],
                "buttons": [
                    {"label": "View on Roblox", "url": RobloxActivityApi.game_page(root_place_id)}
                ]
            }

            if bloxstrap_rpc_formatted_data is not None:
                rpc_data.update(bloxstrap_rpc_formatted_data)

            last_bloxstrap_rpc_formatted_data = bloxstrap_rpc_formatted_data
            last_place_id = place_id
            last_rpc_data = rpc_data
            last_timestamp = entry.timestamp
            
            return rpc_data
    
    return deepcopy(STUDIO_DEFAULT)



# region read_log_file()
def read_log_file(mode: Literal["Player", "Studio"]) -> Optional[list[Entry]]:
    log_files: list = [
        os.path.join(ROBLOX_LOGS_DIRECTORY, file)
        for file in os.listdir(ROBLOX_LOGS_DIRECTORY)
        if mode in file and os.path.isfile(os.path.join(ROBLOX_LOGS_DIRECTORY, file))
    ]
    if not log_files:
        return []

    filepath: str = max(log_files, key=os.path.getmtime)

    with open(filepath, "r", encoding="utf-8", errors="replace") as file:
        content: list[str] = file.readlines()
    content.reverse()

    logs: list[Entry] = []
    for line in content:
        try:
            timestamp_string: str = line.split(",")[0]
            timestamp: int = int(datetime.strptime(timestamp_string, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp())
            prefix: str = line.split(" ")[1]
            data: str = " ".join(line.split(" ")[2:])

            entry: Entry = Entry(
                timestamp,
                prefix,
                data
            )
            logs.append(entry)

        except (IndexError, ValueError):
            continue
    
    return logs


# region is_old_log_file()
def is_old_log_file_player(log_file: list[Entry]) -> bool:
    return (log_file[0].prefix == LogData.OldLogFile.prefix and log_file[0].data.startswith(LogData.OldLogFile.startswith)) or (log_file[0].data.startswith(LogData.GameCrash.startswith))


def is_old_log_file_studio(log_file: list[Entry]) -> bool:
    return log_file[0].prefix == StudioLogData.OldLogFile.prefix and log_file[0].data.startswith(StudioLogData.OldLogFile.startswith)