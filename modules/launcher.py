import os
import sys
from typing import Literal

from modules.info import ProjectData
from modules.filesystem import Directory
from modules.functions.restore_from_mei import restore_from_mei

import customtkinter as ctk


IS_FROZEN = getattr(sys, "frozen", False)

icon_path_extension: str = os.path.join("resources", "favicon.ico")
icon_path: str | None = os.path.join(Directory.root(), icon_path_extension)
if isinstance(icon_path, str):
    if not os.path.isfile(icon_path):
        if IS_FROZEN:
            restore_from_mei(icon_path)
        else:
            icon_path = None

theme_path_extension: str = os.path.join("resources", "theme.json")
theme_path: str = os.path.join(Directory.root(), theme_path_extension)
if not os.path.isfile(theme_path):
    try:
        restore_from_mei(theme_path)
    except Exception as e:
        theme_path = "blue"


class MainWindow:
    root: ctk.CTk

    width: int = 520
    height: int = 320
    size: str = f"{width}x{height}"

    navigation_width: int = 250

    title: str = "Launcher"
    icon: str = icon_path
    theme: str = theme_path
    appearance: str = "System"

    def __init__(self, mode: Literal["WindowsPlayer", "WindowsStudio"]) -> None:
        ctk.set_appearance_mode(self.appearance)
        ctk.set_default_color_theme(self.theme)

        self.root = ctk.CTk()
        self.root.title(self.title)
        self.root.geometry(self.size)
        self.root.minsize(self.width, self.height)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.root.geometry(f"{self.size}+{x}+{y}")

        if self.icon:
            self.root.iconbitmap(self.icon)
        
        ctk.CTkLabel(
            self.root,
            text="Launcher!",
            font=ctk.CTkFont(weight="bold", size=16)
        ).pack(expand=True, fill=ctk.BOTH)
    

    def show(self) -> None:
        self.root.mainloop()