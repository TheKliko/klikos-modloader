import time
import logging
from pypresence import Presence, DiscordNotFound, PipeClosed

from modules.other.api import Api


class Presence:
    CLIENT_ID: str = '1278348258376286268'


    
    def __init__(self) -> None:
        logging.info('Starting Discord RPC . . .')

        try:
            self.pypresence = Presence(self.CLIENT_ID)
        except Exception as e:
            self._on_error(e)


    def start(self) -> None:
        try:
            self.pypresence.connect()
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


    def _on_error(self, exception) -> None:
        if type(exception) in [DiscordNotFound, PipeClosed]:
            logging.warning(f'[{type(exception).__name__}] Retrying in 10 seconds . . .')
            time.sleep(10)
            self.__init__()

        else:
            logging.error(f'[RichPresenceError] [{type(exception).__name__}] {str(exception)}')
            logging.info(f'Stopping Discord RPC . . .')
            self.stop()
    

    def stop(self) -> None:
        if self.presence != None:
            self.presence.close()