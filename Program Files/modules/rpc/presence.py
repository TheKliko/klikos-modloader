import logging
import time
import pypresence
import copy
import threading

from modules.info import Project, URL

from .cooldown import COOLDOWN


class Presence:
    CLIENT_ID: str = "1280969971303841924"
    presence: pypresence.Presence = None
    rpc_updates_paused: bool = False
    rpc_update: bool = False
    force_rpc_update: bool = False

    current_data: dict = {}
    old_data: dict = {}
    default_data: dict = {
        "details": Project.NAME,
        "state": Project.VERSION,
        "large_image": "modloader",
        "buttons": [{"label": "Learn More", "url": URL.GITHUB}]
    }

    _stop_event = threading.Event()


    def __init__(self) -> None:
        logging.info("Starting Discord RPC . . .")
        self.presence = pypresence.Presence(self.CLIENT_ID)


    def _on_error(self, e: Exception) -> None:
        logging.error(type(e).__name__+": "+str(e))
        self.stop()

        if isinstance(e, pypresence.DiscordNotFound):
            logging.info("Retrying in 60 seconds . . .")
            time.sleep(60)
            self.start()
            self.rpc_updates_paused = False
            self.force_rpc_update = True
        
        elif isinstance(e, pypresence.PipeClosed):
            logging.info("Retrying in 15 seconds . . .")
            time.sleep(15)
            self.start()
            self.rpc_updates_paused = False
            self.force_rpc_update = True


    def _default(self) -> None:
        self._update(
            default=True
        )


    def _update(self, default: bool = False) -> None:
        logging.info("Updating RPC status . . .")
        try:
            self.presence.update(
                details=self.current_data.get("details", None) if default == False else self.default_data.get("details", None),
                state=self.current_data.get("state", None) if default == False else self.default_data.get("state", None),
                start=self.current_data.get("start", None) if default == False else self.default_data.get("start", None),
                end=self.current_data.get("end", None) if default == False else self.default_data.get("end", None),
                buttons=self.current_data.get("buttons", None) if default == False else self.default_data.get("buttons", None),
                large_image=self.current_data.get("large_image", None) if default == False else self.default_data.get("large_image", None),
                large_text=self.current_data.get("large_text", None) if default == False else self.default_data.get("large_text", None),
                small_image=self.current_data.get("small_image", None) if default == False else self.default_data.get("small_image", None),
                small_text=self.current_data.get("small_text", None) if default == False else self.default_data.get("small_text", None)
            )
        except Exception as e:
            self._on_error(e)


    def _mainloop(self) -> None:
        self._default()
        while not self._stop_event.is_set():
            if self.rpc_updates_paused == True:
                pass
            elif self.force_rpc_update == True:
                self.force_rpc_update = False
                self._update()
            elif self.current_data != self.old_data:
                self._update()
                self.old_data = copy.deepcopy(self.current_data)
            time.sleep(COOLDOWN)

    

    def update_data(self, data: dict) -> None:
        self.current_data = data


    def start(self) -> None:
        try:
            self.presence.connect()
            if self._stop_event.is_set():
                self._stop_event.clear()

            thread = threading.Thread(
                name="rpc-mainloop",
                target=self._mainloop,
                daemon=True
            )
            thread.start()
        except Exception as e:
            self._on_error(e)
    

    def stop(self) -> None:
        logging.info("Stopping Discord RPC . . .")
        try:
            self.rpc_updates_paused = True
            self._stop_event.set()
            self.presence.close()
        except Exception as e:
            logging.error(type(e).__name__+": "+str(e))