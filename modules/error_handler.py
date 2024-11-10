import sys
import traceback

from modules.logger import logger
from modules.info import Hyperlink, ProjectData

from tkinter import messagebox

IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    import pyi_splash


def run(*args) -> None:
    logger.critical(f"Uncaught exception!")
    logger.debug("\n\n"+"".join(traceback.format_exception(*args)))
    logger.info(f"If you need any help, please join our Discord server: {Hyperlink.DISCORD}")

    if IS_FROZEN:
        if pyi_splash.is_alive():
            pyi_splash.close()

    try:
        messagebox.showerror(f"{ProjectData.NAME} ({ProjectData.VERSION})", f"Uncaught exception!\n\n{''.join(traceback.format_exception(*args))}\nMore information may be available in the latest log file")
    except Exception as e:
        print(f"Uncaught exception!\n\n{''.join(traceback.format_exception(*args))}\nMore information may be available in the latest log file")
    
    sys.exit(1)