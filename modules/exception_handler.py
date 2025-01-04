import sys
import traceback
from tkinter.messagebox import showerror

from modules import Logger
from modules.info import ProjectData, Help


def run(e: Exception) -> None:
    formatted_traceback: str = "".join(traceback.format_exception(e))
    shortened_traceback: str = "".join(traceback.format_exception_only(e))

    Logger.critical(f"\n\n{formatted_traceback}\n")
    Logger.info(f"If you need any help, please join the official support server: {Help.DISCORD}")

    if getattr(sys, "frozen", False):
        try:
            import pyi_splash
            if pyi_splash.is_alive():
                pyi_splash.close()
        except (ModuleNotFoundError, ImportError):
            pass
    
    showerror(title=f"{ProjectData.NAME} ({ProjectData.VERSION})", message=f"{shortened_traceback}\nMore information may be available in the latest log file")
    
    sys.exit(1)