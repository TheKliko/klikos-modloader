import logging
import subprocess
import sys
import time


def launch_roblox(filepath: str) -> None:
    command = get_launch_command(filepath=filepath)
    logging.info("command: "+str(command))
    subprocess.Popen(command)


def get_launch_command(filepath: str) -> str:
    sys_args = sys.argv[2:]

    command: str = "\""+str(filepath)+"\" "
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
        launch_args = "+".join(["launchtime:"+str(int(time.time()*1000)) if item.startswith("launchtime:") else item for item in sys_args[0].split("+")])
        return command+launch_args
    return command