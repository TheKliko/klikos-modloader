from typing import Literal
from pathlib import Path
import ctypes
import json

from modules import Logger
from modules.info import ProjectData
from modules.config import special_settings
from modules.filesystem import Directory, restore_from_meipass
from modules.filesystem.exceptions import FileRestoreError
from modules.functions.interface.image import load as load_image

import customtkinter as ctk


class MainWindow(ctk.CTk):
    class Constants:
        WIDTH: int = 520
        HEIGHT: int = 320
        FAVICON: Path = Directory.RESOURCES / "favicon.ico"
        PLAYER_LOGO: Path = Directory.RESOURCES / "launcher" / "player.png"
        STUDIO_LOGO: Path = Directory.RESOURCES / "launcher" / "studio.png"
    
    class WindowMovement:
        start_x: int
        start_y: int
    
    mode: Literal["Player", "Studio"]
    theme_file: Path
    canceled: bool = False
    border: ctk.CTkFrame
    fg_color: str | tuple[str, str]
    border_color: str | tuple[str, str]


    def __init__(self, mode: Literal["Player", "Studio"]) -> None:
        self.mode = mode

        selected_appearance: str = special_settings.get_value("appearance")
        ctk.set_appearance_mode(selected_appearance)
        
        selected_theme: str = special_settings.get_value("theme")
        theme_file: Path = Directory.THEMES / f"{selected_theme}.json"
        if not theme_file.is_file() and selected_theme != "default":
                try:
                    restore_from_meipass(theme_file)
                except FileRestoreError:
                    Logger.info("Theme file not found, reverting to default theme!", prefix="interface.MainWindow.__init__()")
                    special_settings.set_value("theme", "default")
                    theme_file = Directory.THEMES / "default.json"
        if not theme_file.is_file():
            restore_from_meipass(theme_file)
        ctk.set_default_color_theme(theme_file.resolve())
        self.theme_file = theme_file

        super().__init__()
        self.title(ProjectData.NAME)
        self.resizable(False, False)
        if not self.Constants.FAVICON.is_file():
            restore_from_meipass(self.Constants.FAVICON)
        self.iconbitmap(self.Constants.FAVICON.resolve())

        # Hide the titlebar
        self.overrideredirect(True)
        self._restore_taskbar_icon()
        
        # Allow window movement
        self.bind("<ButtonPress-1>", self._set_window_start_position)
        self.bind("<B1-Motion>", self._do_window_movement)

        self._set_fg_bg_color()
        self._add_content()
        self.geometry(self._get_geometry())
    

    def _set_fg_bg_color(self) -> None:
        try:
            with open(self.theme_file) as file:
                data: dict = json.load(file)
            self.fg_color = data["CTk"]["fg_color"]
            self.border_color = data["CTkFrame"]["border_color"]

        except Exception:
            self.fg_color = ("#f8f8f8", "#1c1c1c")
            self.border_color = ("gray65", "gray28")


    def _add_content(self) -> None:
        if not self.Constants.PLAYER_LOGO.is_file():
            restore_from_meipass(self.Constants.PLAYER_LOGO)
        if not self.Constants.STUDIO_LOGO.is_file():
            restore_from_meipass(self.Constants.STUDIO_LOGO)

        self.border: ctk.CTkFrame = ctk.CTkFrame(self, fg_color=self.border_color, corner_radius=0)
        self.border.pack(fill="both", expand=True)
        
        content: ctk.CTkFrame = ctk.CTkFrame(self.border, fg_color=self.fg_color, corner_radius=0)
        content.pack(fill="both", expand=True, padx=1, pady=1)

        self.versioninfovariable: ctk.StringVar = ctk.StringVar(value="")
        info_label: ctk.CTkLabel = ctk.CTkLabel(content, textvariable=self.versioninfovariable, justify="left", font=ctk.CTkFont(size=13))
        info_label.place(x=20, y=10)

        logo: ctk.CTkLabel
        if self.mode == "Player":
            logo = ctk.CTkLabel(content, text="", image=load_image(self.Constants.PLAYER_LOGO, size=(122,122)))
        elif self.mode == "Studio":
            logo = ctk.CTkLabel(content, text="", image=load_image(self.Constants.STUDIO_LOGO, size=(122,122)))
        logo.place(x=(self.Constants.WIDTH // 2) - (122 // 2), y=56)

        self.textvariable: ctk.StringVar = ctk.StringVar(value="")
        label: ctk.CTkLabel = ctk.CTkLabel(content, textvariable=self.textvariable, width=self.Constants.WIDTH, font=ctk.CTkFont(size=14))
        label.place(x=0, y=203)

        progress_bar: ctk.CTkProgressBar = ctk.CTkProgressBar(content, mode="indeterminate", corner_radius=0, width=460, height=20)
        progress_bar.place(x=(self.Constants.WIDTH // 2) - (460 // 2), y=245)
        progress_bar.start()

        close_button = ctk.CTkButton(content, text="Cancel", width=130, height=34, corner_radius=2, command=self._on_cancel)
        close_button.place(x=(self.Constants.WIDTH // 2) - (130 // 2), y=273)


    def _restore_taskbar_icon(self) -> None:  # Generated by ChatGPT
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)  # GWL_EXSTYLE = -20
        style &= ~0x00000080  # Remove WS_EX_TOOLWINDOW
        style |= 0x00000000  # Add WS_EX_APPWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)
        ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x27)  # SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_FRAMECHANGED


    def _get_geometry(self) -> str:
        x: int = (self.winfo_screenwidth() // 2) - (self.Constants.WIDTH // 2)
        y: int = (self.winfo_screenheight() // 2) - (self.Constants.HEIGHT // 2)
        return f"{self.Constants.WIDTH}x{self.Constants.HEIGHT}+{x}+{y}"


    def _set_window_start_position(self, event) -> None:
        self.WindowMovement.start_x = event.x
        self.WindowMovement.start_y = event.y


    def _do_window_movement(self, event) -> None:
        x = self.winfo_x() + event.x - self.WindowMovement.start_x
        y = self.winfo_y() + event.y - self.WindowMovement.start_y
        self.geometry(f"+{x}+{y}")
    

    def _on_close(self, *args, **kwargs) -> None:
        self.after(1, self.destroy)
    

    def _on_cancel(self) -> None:
        self.canceled = True
        self._on_close()
    

    def bring_to_top(self) -> None:
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)
