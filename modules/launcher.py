import os
import sys
import threading
from typing import Literal, Callable

from modules.info import ProjectData
from modules.filesystem import Directory
from modules.interface.images import load_image
from modules.functions.restore_from_mei import restore_from_mei, FileRestoreError

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


# region MainWindow
class MainWindow:
    root: ctk.CTk
    mode: str

    width: int = 520
    height: int = 320
    size: str = f"{width}x{height}"

    title: str = "Launcher"
    icon: str | None = icon_path
    theme: str = theme_path
    appearance: str = "System"

    textvar: ctk.StringVar
    image_size: tuple[int, int] = (128, 128)

    font_bold: ctk.CTkFont
    font_title: ctk.CTkFont
    font_subtitle: ctk.CTkFont
    font_small: ctk.CTkFont
    font_small_bold: ctk.CTkFont
    font_13: ctk.CTkFont
    font_13_bold: ctk.CTkFont
    font_navigation: ctk.CTkFont
    font_medium_bold: ctk.CTkFont
    font_large: ctk.CTkFont
    font_large_italic: ctk.CTkFont
    font_large_bold: ctk.CTkFont

    def __init__(self, mode: Literal["WindowsPlayer", "WindowsStudio"]) -> None:
        ctk.set_appearance_mode(self.appearance)
        ctk.set_default_color_theme(self.theme)

        self.root = ctk.CTk()
        self.root.title(self.title)
        self.root.geometry(self.size)
        self.root.minsize(self.width, self.height)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.root.geometry(f"{self.size}+{x}+{y}")

        if self.icon:
            self.root.iconbitmap(self.icon)
        
        self.font_bold = ctk.CTkFont(weight="bold")
        self.font_title = ctk.CTkFont(size=20, weight="bold")
        self.font_large = ctk.CTkFont(size=16)
        self.font_large_italic = ctk.CTkFont(size=16, slant="italic")
        self.font_large_bold = ctk.CTkFont(size=16, weight="bold")
        self.font_subtitle = ctk.CTkFont(size=16, weight="bold")
        self.font_small = ctk.CTkFont(size=12)
        self.font_small_bold = ctk.CTkFont(size=12, weight="bold")
        self.font_13 = ctk.CTkFont(size=13)
        self.font_13_bold = ctk.CTkFont(size=13, weight="bold")
        self.font_medium_bold = ctk.CTkFont(size=14, weight="bold")
        self.font_navigation = ctk.CTkFont()
        
        self.mode = mode

        # Logo
        launcher_logo: str = os.path.join(Directory.root(), "resources", "launcher", "icon.png")
        if not os.path.isfile(launcher_logo):
            try:
                restore_from_mei(launcher_logo)
            except (FileRestoreError, PermissionError, FileNotFoundError):
                pass
        ctk.CTkLabel(
            self.root,
            text="",
            image=load_image(
                launcher_logo,
                launcher_logo,
                self.image_size
            )
        ).grid(column=0, row=0, padx=32, pady=(32,16))

        # Text
        self.textvar = ctk.StringVar(value=". . .")
        ctk.CTkLabel(
            self.root,
            textvariable=self.textvar,
            font=self.font_large
        ).grid(column=0, row=1, padx=32)

        # Progress bar
        progress_bar: ctk.CTkProgressBar = ctk.CTkProgressBar(
            self.root,
            mode="indeterminate",
            width=256
        )
        progress_bar.grid(column=0, row=2, padx=32, pady=(16,32))
        progress_bar.start()

        self.root.update_idletasks()
        # width = self.root.winfo_reqwidth()
        # height = self.root.winfo_reqheight()
        width = self.width
        height = self.height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)
    

    def show(self) -> None:
        threading.Thread(
            name="launcher-main-thread",
            target=worker,
            args=(self.textvar, self.close),
            daemon=True
        ).start()
        self.root.mainloop()

    def close(self) -> None:
        self.root.destroy()


def worker(textvariable: ctk.StringVar, close_window_function: Callable) -> None:
    import time
    textvariable.set("Testing . . .")
    time.sleep(2)
    textvariable.set("Launching Roblox . . .")
    time.sleep(2)
    close_window_function()