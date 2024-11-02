import time
import threading
from copy import deepcopy
from typing import Literal, Optional

from modules.logger import logger
from modules.info import ProjectData, Hyperlink

from pypresence import Presence, DiscordNotFound, PipeClosed


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

    MAINLOOP_COOLDOWN: float = 0.1
    DISCORDNOTFOUND_COOLDOWN: int = 30
    PIPECLOSED_COOLDOWN: int = 15

    mode: str

    DEFAULT: dict = {
        "start": None,
        "end": None,
        "details": ProjectData.NAME,
        "state": f"Version {ProjectData.VERSION}",
        "large_image": ASSET_KEYS["default"],
        "large_image_text": ProjectData.NAME,
        "small_image": None,
        "small_image_text": None,
        "buttons": [{"label": "Learn More", "url": Hyperlink.GITHUB}]
    }
    current: dict = deepcopy(DEFAULT)
    last: Optional[dict] = None


    def __init__(self, mode: Literal["WindowsPlayer", "WindowsStudio"]) -> None:
        self.mode = mode
        self.client = Presence(self.CLIENT_ID)
        logger.info("RPC client is ready!")


    def _connect(self) -> None:
        if not self._connected:
            return

        logger.info("Starting Discord RPC...")
        try:
            self.client.connect()
            self._connected = True
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
        if not self._connected:
            self._connect()

        try:
            while not self._stop_event.is_set():
                if self.current != self.last:
                    try:
                        logger.info("Updating RPC status...")
                        self.client.update(**self.current)
                        self.last = deepcopy(self.current)
                    except PipeClosed:
                        logger.error(f"Discord pipe closed! Retrying in {self.PIPECLOSED_COOLDOWN} seconds...")
                        self._connected = False
                        self._connect()
                time.sleep(self.MAINLOOP_COOLDOWN)
        
        except Exception as e:
            logger.error(f"RPC Error! {type(e).__name__}: {e}")

        self._stop()


    def start(self) -> None:
        threading.Thread(
            name="rpc-thread-mainloop",
            target=self._mainloop,
            daemon=True
        ).start()


    def stop(self) -> None:
        self._stop_event.set()
        time.sleep(0.1)
        self._stop()