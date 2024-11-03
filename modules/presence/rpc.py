import time
import threading
from copy import deepcopy
from typing import Literal, Optional

from modules.logger import logger
from modules.info import ProjectData, Hyperlink
from modules.functions.config import integrations

from pypresence import Presence, DiscordNotFound, PipeClosed

from . import logs


class DiscordRPC:
    client: Presence
    CLIENT_ID: str = "1280969971303841924"
    ASSET_KEYS: dict = {
        "default": "modloader",
        "WindowsPlayer": "roblox",
        "WindowsStudio": "studio"
    }
    _connected: bool = False
    _stop_event: threading.Event = threading.Event()
    _launch_confirmed: bool = False

    MAINLOOP_COOLDOWN: float = 0.2
    DISCORDNOTFOUND_COOLDOWN: int = 30
    PIPECLOSED_COOLDOWN: int = 15

    mode: Literal["WindowsPlayer", "WindowsStudio"]

    DEFAULT: dict = {
        "start": None,
        "end": None,
        "details": ProjectData.NAME,
        "state": f"Version {ProjectData.VERSION}",
        "large_image": ASSET_KEYS["default"],
        "large_text": ProjectData.NAME,
        "small_image": None,
        "small_text": None,
        "buttons": [{"label": "Learn More", "url": Hyperlink.GITHUB}]
    }
    current: Optional[dict] = None
    last: Optional[dict] = None


    def __init__(self, mode: Literal["WindowsPlayer", "WindowsStudio"]) -> None:
        self.mode = mode
        self.client = Presence(self.CLIENT_ID)
        logger.info("RPC client is ready!")


    def _connect(self) -> None:
        logger.info("Starting Discord RPC...")
        try:
            self.client.connect()
            self._connected = True
            self.client.update(**self.DEFAULT)
        except DiscordNotFound as e:
            logger.info(f"Discord client not found! Retrying in {self.DISCORDNOTFOUND_COOLDOWN} seconds...")
            time.sleep(self.DISCORDNOTFOUND_COOLDOWN)
        except Exception as e:
            logger.info(f"RPC client failed to connect! {type(e).__name__}: {e}")
            self._stop_event.set()
    

    def _stop(self) -> None:
        logger.info("Stopping Discord RPC...")
        self._stop_event.set()

        try:
            self.client.close()
        except Exception as e:
            logger.error(f"Error while stopping RPC! {type(e).__name__}: {e}")


    def _mainloop(self) -> None:
        self._connect()

        try:
            while not self._stop_event.is_set():
                time.sleep(self.MAINLOOP_COOLDOWN)

                if not integrations.value("discord_rpc"):
                    self._stop()

                self.current: Optional[dict] = logs.read(self.mode)
                if self.current is None and self._launch_confirmed is True:
                    self._stop_event.set()
                    break
                
                elif self.current is None:
                    continue

                self._launch_confirmed = True

                if self.current != self.last:
                    try:
                        logger.info("Updating RPC status...")
                        self.client.update(**self.current)
                        self.last = deepcopy(self.current)
                    except PipeClosed:
                        logger.error(f"Discord pipe closed! Retrying in {self.PIPECLOSED_COOLDOWN} seconds...")
                        self._connected = False
                        time.sleep(self.PIPECLOSED_COOLDOWN)
                        self._connect()
        
        except Exception as e:
            logger.error(f"RPC Error! {type(e).__name__}: {e}")

        self._stop()


    def start(self) -> None:
        self._mainloop()


    def stop(self) -> None:
        self._stop_event.set()
        time.sleep(0.1)
        self._stop()