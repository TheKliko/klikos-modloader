from typing import Literal
import time

from modules import Logger
from modules.config import integrations

from .log_reader import LogReader

from pypresence import Presence, DiscordNotFound, PipeClosed


class RichPresenceClient:
    class Constants:
        CLIENT_ID: str = "1280969971303841924"
        CONNECTION_ATTEMPTS: int = 3
        RECONNECT_COOLDOWN: float = 5
        class AssetKeys:
            DEFAULT: str = "modloader"
            PLAYER: str = "roblox"
            STUDIO: str = "studio"
        COOLDOWN: float = 0.2
    
    mode: Literal["Player", "Studio"]
    client: Presence
    timestamp: int = 1
    connected: bool = False
    launched: bool = False
    log_reader: LogReader
    last_update: int = 0
    last_status: dict | Literal["DEFAULT"] = {}


    def __init__(self, mode: Literal["Player", "Studio"]) -> None:
        self.mode = mode
        self.log_reader = LogReader(mode)
        Logger.info("Log reader is ready!")
        self.client = Presence(self.Constants.CLIENT_ID)
        Logger.info("Client is ready!")


    def connect(self) -> None:
        Logger.info("Connecting client...")

        exception: Exception = None
        for _ in range(self.Constants.CONNECTION_ATTEMPTS):
            try:
                self.client.connect()
                self.connected = True
                Logger.info("Client connected successfully!")
                return

            except Exception as e:
                Logger.error(f"Client failed to connect! {type(e).__name__}: {e}")
                exception = e
                time.sleep(self.Constants.RECONNECT_COOLDOWN)

        raise exception


    def mainloop(self) -> None:
        self._confirm_roblox_launch()
        self.launched = True
        self._set_default_status()
        while True:
            if not integrations.get_value("discord_rpc"):
                Logger.warning("Discord RPC turned off!")
                break

            new_status: dict | Literal["DEFAULT"] = self.log_reader.get_status()

            time.sleep(self.Constants.COOLDOWN)
            break


    def _set_default_status(self) -> None:
        self.client.update(
            start=self.timestamp,
            end=None,
            details=f"Roblox {self.mode}",
            state="Browsing..." if self.mode == "Player" else "Idling...",
            large_image=self.Constants.AssetKeys.PLAYER if self.mode == "Player" else self.Constants.AssetKeys.STUDIO,
            large_text=f"Roblox {self.mode}",
            small_image=None,
            small_text=None,
            buttons=None
        )