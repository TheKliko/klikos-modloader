import sys
import time
import subprocess

from modules import Logger


def launch_roblox(filepath: str) -> None:
    command = get_launch_command(filepath)
    Logger.info(f"Launch command: {command}")
    subprocess.Popen(command)


def get_launch_command(filepath: str) -> str:
    sys_args = sys.argv[2:]
    command: str = f"\"{filepath}\""

    if not sys_args:
        return command

    timestamp: int = int(time.time()*1000)
    launch_args = "+".join(
        [
        f"launchtime:{timestamp}" if item.startswith("launchtime:") else item
        for item in sys_args[0].split("+")
        ]
    )
    return f"{command} {launch_args}"