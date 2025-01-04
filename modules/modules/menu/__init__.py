from modules import Logger

from .main_window import MainWindow


def run() -> None:
    Logger.debug("Running menu...")

    window: MainWindow = MainWindow()
    window.mainloop()