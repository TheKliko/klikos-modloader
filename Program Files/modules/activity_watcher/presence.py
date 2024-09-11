import time
import logging
from pypresence import Presence, DiscordNotFound, PipeClosed

from modules.other.api import Api
from modules.utils import variables

from .presence_default import DefaultRPC


class RichPresence:
    CLIENT_ID: str = '1280969971303841924'
    pypresence = None


    
    def __init__(self) -> None:
        logging.info('Starting Discord RPC . . .')

        try:
            self.pypresence = Presence(self.CLIENT_ID)
        except Exception as e:
            self._on_error(e)
    

    def _init(self) -> None:
        logging.info('Starting Discord RPC . . .')

        try:
            self.pypresence = Presence(self.CLIENT_ID)
        except Exception as e:
            self._on_error(e)


    def _on_error(self, exception) -> None:
        if type(exception) in [DiscordNotFound, PipeClosed]:
            logging.warning(f'[{type(exception).__name__}] Retrying in 5 seconds . . .')

            self._init()
            time.sleep(5)
            self.start()
            variables.set('do_rpc_update', True)

        else:
            logging.error(f'[RichPresenceError] [{type(exception).__name__}] {str(exception)}')
            logging.info(f'Stopping Discord RPC . . .')
            self.stop()
    

    def _set_default(self) -> None:
        binary_type: str = variables.get('binary_type', 'WindowsPlayer')
        if binary_type.endswith('Studio'):
            details = DefaultRPC.ROBLOX_STUDIO_DETAILS
            large_image=DefaultRPC.ROBLOX_STUDIO_LARGE_IMAGE
            large_text=DefaultRPC.ROBLOX_STUDIO_LARGE_TEXT
        else:
            details = DefaultRPC.ROBLOX_PLAYER_DETAILS
            large_image=DefaultRPC.ROBLOX_PLAYER_LARGE_IMAGE
            large_text=DefaultRPC.ROBLOX_PLAYER_LARGE_TEXT
        self.update(
            details=details,
            state=DefaultRPC.STATE,
            large_image=large_image,
            large_text=large_text,
            small_image = DefaultRPC.SMALL_IMAGE,
            small_text = DefaultRPC.SMALL_TEXT,
        )


    def start(self) -> None:
        try:
            self.pypresence.connect()
            self._set_default()
        except Exception as e:
            self._on_error(e)


    def update(
            self,
            details: str = None,
            state: str = None,
            large_image: str = None,
            large_text: str = None,
            small_image: str = None,
            small_text: str = None,
            start: str = None,
            end: str = None,
            buttons: list[dict[str, str]] = None
        ) -> None:
        try:
            self.pypresence.update(
                details=details,
                state=state,
                large_image=large_image,
                large_text=large_text,
                small_image=small_image,
                small_text=small_text,
                start=start,
                end=end,
                buttons=buttons
            )
        except Exception as e:
            self._on_error(e)
    

    def stop(self) -> None:
        if isinstance(self.pypresence, Presence):
            self.pypresence.close()