import sys
import traceback

from modules.logger import logger
from modules.info import Hyperlink, ProjectData

from tkinter import messagebox

IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    import pyi_splash


def run(e: Exception) -> None:

    logger.critical(f"Uncaught exception! {type(e).__name__}: {e}")
    logger.debug("".join(traceback.format_exception(type(e), e, e.__traceback__)))
    logger.info(f"If you need any help, please join our Discord server: {Hyperlink.DISCORD}")

    if IS_FROZEN:
        if pyi_splash.is_alive():
            pyi_splash.close()

    messagebox.showerror(f"{ProjectData.NAME} ({ProjectData.VERSION})", message=f"Uncaught exception!\n{type(e).__name__}: {e}\n\n{''.join(traceback.format_exception(type(e), e, e.__traceback__))}\nMore information may be available in the latest log file")