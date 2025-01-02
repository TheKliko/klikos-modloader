import sys
import time
import traceback
from typing import Literal, Optional

from modules import Logger
from modules.info import Help
from modules.filesystem import Directory
from modules.config import integrations
from modules.functions.process_exists import process_exists

from .rpc import RichPresenceClient, DiscordNotFound
from .exceptions import RobloxNotLaunched


def run(mode: Optional[Literal["Player", "Studio"]] = None) -> None:
    Logger.info("Running RPC module...")
    if not integrations.get_value("discord_rpc"):
        Logger.warning("Discord RPC is disabled!")
        return
    
    print(Directory.LOCALAPPDATA)
    if not Directory.LOCALAPPDATA.is_dir():
        Logger.error("Failed to start RPC module! %LOCALAPPDATA% not found")
        return
    
    if not Directory.ROBLOX_LOGS.is_dir():
        Logger.error("Failed to start RPC module! Roblox logs directory not found")
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
        Logger.warning("No existing Roblox instances! Stopping RPC module...")
        return
    
    try:
        client: RichPresenceClient = RichPresenceClient(mode)
        try:
            client.connect()
        except DiscordNotFound:
            Logger.warning(f"Discord not found!")
            return
        client.mainloop()
    
    except RobloxNotLaunched as e:
        Logger.error(str(e))
    
    except Exception as e:
        formatted_traceback: str = "".join(traceback.format_exception(e))
        Logger.critical(f"RPC Error!\n\n{formatted_traceback}\n")
        Logger.info(f"If you need any help, please join the official support server: {Help.DISCORD}")


def get_rpc_mode(attempts: int = 5) -> Literal["Player", "Studio"] | None:
    for i in range(attempts):
        if process_exists("RobloxPlayerBeta.exe"):
            return "Player"
        elif process_exists("eurotrucks2.exe"):
            return "Player"
        elif process_exists("RobloxStudioBeta.exe"):
            return "Studio"
        time.sleep(1)
    return None