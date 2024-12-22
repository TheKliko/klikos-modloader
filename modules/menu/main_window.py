from pathlib import Path

from modules import Logger
from modules import exception_handler
from modules.info import ProjectData
from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image

from .navigation import NavigationFrame

import customtkinter as ctk


class MainWindow(ctk.CTk):
    class Constants:
        WIDTH: int = 1100
        HEIGHT: int = 600
        THEME: Path = Directory.RESOURCES / "theme.json"
        FAVICON: Path = Directory.RESOURCES / "favicon.ico"


    def __init__(self) -> None:
        ctk.set_appearance_mode("System")
        if not self.Constants.THEME.is_file():
            restore_from_meipass(self.Constants.THEME)
        ctk.set_default_color_theme(self.Constants.THEME.resolve())

        super().__init__()
        self.title(ProjectData.NAME)
        self.resizable(False, False)
        if not self.Constants.FAVICON.is_file():
            restore_from_meipass(self.Constants.FAVICON)
        self.iconbitmap(self.Constants.FAVICON.resolve())

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.navigation: NavigationFrame = NavigationFrame(self)
        self.navigation.grid(column=0, row=0, sticky="nsew")

        self.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        self.report_callback_exception = self._on_error

        self.geometry(self._get_geometry())


    def _get_geometry(self) -> str:
        x: int = (self.winfo_screenwidth() // 2) - (self.Constants.WIDTH // 2)
        y: int = (self.winfo_screenheight() // 2) - (self.Constants.HEIGHT // 2)
        return f"{self.Constants.WIDTH}x{self.Constants.HEIGHT}+{x}+{y}"
    

    def _on_close(self, *args, **kwargs) -> None:
        self.after(1, self.destroy)
    

    def _on_error(self, exception_class, exception, traceback) -> None:
        exception_handler.run(exception)
        self._on_close()