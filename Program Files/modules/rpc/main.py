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
from modules.rpc import presence


def main() -> None:
    logger.start(filename="RPC")

    try:
        pass
        import time
        from activity_watcher import ActivityWatcher, StudioActivityWatcher
        from cooldown import COOLDOWN

        mode = wait_until_roblox_is_launched.any()
        if not mode:
            sys.exit()

        rpc = presence.Presence()
        rpc.start()

        activity_watcher = ActivityWatcher() if mode == "player" else StudioActivityWatcher()
        while not activity_watcher._stop_event.is_set():
            time.sleep(COOLDOWN)
            if mode == "player":
                if not wait_until_roblox_is_launched.process_exists("RobloxPlayerBeta.exe"):
                    activity_watcher._stop_event.set()
                    break
            elif mode == "studio":
                if not wait_until_roblox_is_launched.process_exists("RobloxStudioBeta.exe"):
                    activity_watcher._stop_event.set()
                    break

            data: dict = activity_watcher.get_data()
            rpc.update_data(data)

        rpc.stop()
    
    except Exception as e:
        logging.error(type(e).__name__+": "+str(e))
        raise


if __name__ == "__main__":
    main()