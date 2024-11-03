import os
import json
from copy import deepcopy
from typing import Optional, Literal

from modules.request import RobloxActivityApi
from modules.filesystem import Directory
from modules.functions.config import integrations

from .data import LogData, StudioLogData


class Entry:
    def __init__(self, prefix: str, data: str) -> None:
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
    "details": "Playing Roblox",
    "state": "Idling...",
    "large_image": "studio",
    "large_text": "Roblox Studio",
    "small_image": None,
    "small_text": None,
    "buttons": None
}


# region Player
def player() -> Optional[dict]:
    allow_activity_joining: Optional[bool] = integrations.value("activity_joining")

    log_file: Optional[list[Entry]] = read_log_file("Player")
    if not log_file:
        return None
    
    if log_file[0].prefix == LogData.OldLogFile.prefix and log_file[0].data.startswith(LogData.OldLogFile.startswith):
        return None
    
    for entry in log_file:
        is_game_joining: bool = entry.prefix == LogData.GameJoining.prefix and entry.data.startswith(LogData.GameJoining.startswith)
        is_game_join: bool = entry.prefix == LogData.GameJoin.prefix and entry.data.startswith(LogData.GameJoin.startswith)
        is_game_leave: bool = entry.prefix == LogData.GameLeave.prefix and entry.data.startswith(LogData.GameLeave.startswith)

        if is_game_leave:
            return deepcopy(PLAYER_DEFAULT)
    
    return deepcopy(PLAYER_DEFAULT)



# region Studio
def studio() -> Optional[dict]:
    log_file: Optional[list[Entry]] = read_log_file("Studio")
    if not log_file:
        return None
    
    if log_file[0].prefix == LogData.OldLogFile.prefix and log_file[0].data.startswith(LogData.OldLogFile.startswith):
        return None
    
    for entry in log_file:
        is_game_join: bool = entry.prefix == StudioLogData.GameJoin.prefix and entry.data.startswith(StudioLogData.GameJoin.startswith)
        is_game_leave: bool = entry.prefix == StudioLogData.GameLeave.prefix and entry.data.startswith(StudioLogData.GameLeave.startswith)
        is_bloxstrap_rpc: bool = entry.prefix == StudioLogData.BloxstrapRPC.prefix and entry.data.startswith(StudioLogData.BloxstrapRPC.startswith)

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

                return {
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
            # region TODO: is_game_join
    
    return deepcopy(STUDIO_DEFAULT)



# region Read logs
def read_log_file(mode: Literal["Player", "Studio"]) -> Optional[list[Entry]]:
    log_files: list = [
        os.path.join(ROBLOX_LOGS_DIRECTORY, file)
        for file in os.listdir(ROBLOX_LOGS_DIRECTORY)
        if mode in file and os.path.isfile(os.path.join(ROBLOX_LOGS_DIRECTORY, file))
    ]
    if not log_files:
        return []

    filepath: str = max(log_files, key=os.path.getmtime)

    with open(filepath, "r", encoding="utf-8") as file:
        content: list[str] = file.readlines()
    content.reverse()

    logs: list[Entry] = []
    for line in content:
        try:
            entry: Entry = Entry(
                line.split(" ")[1],
                " ".join(line.split(" ")[2:])
            )
            logs.append(entry)

        except IndexError:
            continue
    
    return logs