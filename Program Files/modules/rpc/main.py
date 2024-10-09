import os
import sys
import logging

program_files_directory: str = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
python_version: str = str(sys.version_info.major)+"."+str(sys.version_info.minor)
libraries: str = os.path.join(program_files_directory, "libraries", python_version)
os.makedirs(libraries, exist_ok=True)
sys.path.append(libraries)
sys.path.append(program_files_directory)

from modules.startup import logger
from modules.functions import wait_until_roblox_is_launched
import presence
from activity_watcher import ActivityWatcher, StudioActivityWatcher
from cooldown import COOLDOWN


def main() -> None:
    logger.start(filename="RPC")

    try:
        pass
        import time

        mode = wait_until_roblox_is_launched.any()
        if not mode:
            sys.exit()

        rpc = presence.Presence()
        rpc.start()

        activity_watcher = ActivityWatcher() if mode == "player" else StudioActivityWatcher()
        while activity_watcher.stop_rpc == False:
            rpc.update_data(activity_watcher.get_data())
            time.sleep(COOLDOWN)
            break

        rpc.stop()
    
    except Exception as e:
        logging.error(type(e).__name__+": "+str(e))
        raise


if __name__ == "__main__":
    main()