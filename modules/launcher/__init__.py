from typing import Literal
from threading import Thread

from modules import Logger

from .interface import MainWindow
from . import tasks


def run(mode: Literal["Player", "Studio"]) -> None:
    Logger.info(f"Running launcher in mode: {mode}")

    interface: MainWindow = MainWindow(mode)
    Thread(
        name="launcher.tasks.run()_Thread",
        target=tasks.run,
        args=(mode, interface.textvariable, interface._on_close),
        daemon=True
    ).start()

    interface.mainloop()

    # Run activity watcher