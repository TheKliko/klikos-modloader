from threading import Thread

from modules import Logger

from .interface import MainWindow
from . import tasks


def run(mode: str) -> None:
    Logger.info(f"Running launcher in mode: {mode}")
    interface: MainWindow = MainWindow(mode)
    Thread(name="launcher.tasks.run()_Thread", target=tasks.run, args=(interface,), daemon=True).run()
    interface.mainloop()