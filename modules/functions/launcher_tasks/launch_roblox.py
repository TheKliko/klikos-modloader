import sys
import subprocess
import time

from modules.logger import logger


def launch_roblox(target: str) -> None:
    logger.info("Launching Roblox...")
    command = get_launch_command(filepath=target)
    logger.info(f"Launch command: {command}")
    subprocess.Popen(command)


def get_launch_command(filepath: str) -> str:
    sys_args = sys.argv[2:]

    command: str = f"\"{filepath}\""
    if sys_args:
        # args = sys_args[0]
        # if args.startswith("roblox-player") or args.startswith("roblox-studio"):
        #     args_dict: dict = {}
        #     args_data = args.split("+")
        #     for item in args_data:
        #         kv = item.split(":")
        #         args_dict[kv[0]] = kv[1]
        #     args_dict["timestamp"] = int(time.time()*1000)
        #     launch_args: list = []
        #     for k,v in args_dict.items():
        #         launch_args.append(str(k)+":"+str(v))
        #     return command+" "+"+".join(launch_args)
        # return command+" "+args

        timestamp: int = int(time.time()*1000)
        launch_args = "+".join(
            [
            f"launchtime:{timestamp}" if item.startswith("launchtime:") else item
            for item in sys_args[0].split("+")
            ]
        )
        return f"{command} {launch_args}"
    return command