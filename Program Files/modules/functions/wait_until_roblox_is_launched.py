import time
import subprocess
from typing import Literal


def wait_until_roblox_is_launched(mode: Literal["player", "studio"], timeout: int = 180) -> None:
    if mode.lower() not in ["player", "studio"]:
        raise Exception("Mode must be 'player' or 'studio'! not '"+str(mode)+"'")
    
    for i in range(timeout):
        if mode == "player":
            if process_exists("RobloxPlayerBeta.exe") == True:
                return
        elif mode == "studio":
            if process_exists("RobloxStudioBeta.exe") == True:
                return
        time.sleep(1)
    else:
        raise Exception("Roblox did not launch after "+str(timeout)+" seconds")


def any(timeout: int = 180) -> Literal["player", "studio"]|None:
    for i in range(timeout):
        if process_exists("RobloxPlayerBeta.exe") == True:
            return "player"
        elif process_exists("RobloxStudioBeta.exe") == True:
            return "studio"
        time.sleep(1)
    return None


# https://stackoverflow.com/a/29275361
def process_exists(process_name: str) -> bool:
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())