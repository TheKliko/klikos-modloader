import time
from typing import Literal, Optional

from modules.logger import logger
from modules.functions.config import integrations
from modules.functions.process_exists import process_exists

from .rpc import DiscordRPC


def run(mode: Optional[Literal["WindowsPlayer", "WindowsStudio"]]) -> None:
    if not integrations.value("discord_rpc"):
        return
    
    logger.info("Running RPC module...")
    if not mode:
        mode = get_rpc_mode()
        if not mode:
            logger.warning("No existing Roblox instances! Stopping RPC module...")
            return

    rpc = DiscordRPC(mode)
    rpc.start()


def get_rpc_mode() -> Literal["WindowsPlayer", "WindowsStudio"] | None:
    ATTEMPTS: int = 5

    for i in range(ATTEMPTS):
        if process_exists("RobloxPlayerBeta.exe"):
            return "WindowsPlayer"
        elif process_exists("RobloxStudioBeta.exe"):
            return "WindowsStudio"
        time.sleep(1)

    return None