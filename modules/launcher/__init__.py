import os
import sys
import subprocess
from typing import Literal
from threading import Thread
from queue import Queue

from modules import Logger
from modules.config import integrations
from modules import activity_watcher

from .interface import MainWindow
from . import tasks

IS_FROZEN: bool = getattr(sys, "frozen", False)


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

    interface.bring_to_top()
    interface.mainloop()

    if interface.canceled:
        return

    if not exception_queue.empty():
        raise exception_queue.get()

    if not integrations.get_value("discord_rpc"):
        Logger.info("Discord RPC is disabled!")
        return
    
    Logger.info("Starting Discord RPC")
    activity_watcher.run(mode)