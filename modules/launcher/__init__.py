from typing import Literal
from threading import Thread
from queue import Queue

from modules import Logger

from .interface import MainWindow
from . import tasks


def run(mode: Literal["Player", "Studio"]) -> None:
    Logger.info(f"Running launcher in mode: {mode}")

    exception_queue: Queue = Queue(1)

    interface: MainWindow = MainWindow(mode)
    Thread(
        name="launcher.tasks.run()_Thread",
        target=tasks.run,
        args=(mode, interface.textvariable, interface.versioninfovariable, interface._on_close, exception_queue),
        daemon=True
    ).start()

    interface.mainloop()

    if not exception_queue.empty():
        raise exception_queue.get()

    # TODO: Run activity watcher