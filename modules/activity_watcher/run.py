import sys
import time
import traceback
import os
from pathlib import Path
from typing import Literal, Optional

from modules import Logger
from modules.info import Help
from modules.filesystem import Directory
from modules.config import integrations
from modules.functions.process_exists import process_exists

from .rpc import RichPresenceClient, DiscordNotFound
from .exceptions import RobloxNotLaunched


def run(mode: Optional[Literal["Player", "Studio"]] = None) -> None:
    Logger.info("Running RPC module...", prefix="activity_watcher.run()")
    if not integrations.get_value("discord_rpc"):
        Logger.warning("Discord RPC is disabled!", prefix="activity_watcher.run()")
        return
    
    if not Directory.LOCALAPPDATA.is_dir():
        Logger.error("Failed to start RPC module! %LOCALAPPDATA% not found", prefix="activity_watcher.run()")
        return
    
    if not Directory.ROBLOX_LOGS.is_dir():
        Logger.error("Failed to start RPC module! Roblox logs directory not found", prefix="activity_watcher.run()")
        return
    
    # Check launch args for RPC mode
    if not mode:
        args: list[str] = sys.argv[1:]
        if len(args) >= 2:
            mode = args[1] if args[1] in ["Player", "Studio"] else None

    # Look for Roblox process to get RPC mode
    if not mode:
        mode = get_rpc_mode()

    if not mode:
        Logger.warning("No existing Roblox instances! Stopping RPC module...", prefix="activity_watcher.run()")
        return
    
    try:
        client: RichPresenceClient = RichPresenceClient(mode)
        try:
            client.connect()
        except DiscordNotFound:
            Logger.warning(f"Discord not found!", prefix="activity_watcher.run()")
            return
        client.mainloop()
    
    except RobloxNotLaunched as e:
        Logger.error("Could not confirm Roblox launch!")
    
    except Exception as e:
        formatted_traceback: str = "".join(traceback.format_exception(e))
        Logger.critical(f"RPC Error!\n\n{formatted_traceback}\n", prefix="activity_watcher.run()")
        Logger.info(f"If you need any help, please join the official support server: {Help.DISCORD}", prefix="activity_watcher.run()")


def get_rpc_mode(attempts: int = 5) -> Literal["Player", "Studio"] | None:
    for _ in range(attempts):
        if process_exists("RobloxPlayerBeta.exe"):
            return "Player"
        
        elif process_exists("RobloxStudioBeta.exe"):
            return "Studio"
        
        elif process_exists("eurotrucks2.exe"):
            log_files: list[Path] = [
                item
                for item in Directory.ROBLOX_LOGS.iterdir()
                if item.is_file()
            ]
            latest: Path = max(log_files, key=os.path.getmtime)
            if "Player" in latest.name:
                return "Player"
            elif "Studio" in latest.name:
                return "Studio"

        time.sleep(1)
    return None