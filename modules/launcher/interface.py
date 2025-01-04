from typing import Literal
from pathlib import Path

from modules.info import ProjectData
from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image

import customtkinter as ctk


class MainWindow(ctk.CTk):
    class Constants:
        WIDTH: int = 520
        HEIGHT: int = 320
        THEME: Path = Directory.RESOURCES / "theme.json"
        FAVICON: Path = Directory.RESOURCES / "favicon.ico"
        PLAYER_LOGO: Path = Directory.RESOURCES / "launcher" / "player.png"
        STUDIO_LOGO: Path = Directory.RESOURCES / "launcher" / "studio.png"
    
    class WindowMovement:
        start_x: int
        start_y: int
    
    canceled: bool = False


    def __init__(self, mode: Literal["Player", "Studio"]) -> None:
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

        # Hide the titlebar
        self.overrideredirect(True)
        self.bind("<ButtonPress-1>", self._set_window_start_position)
        self.bind("<B1-Motion>", self._do_window_movement)
        
        if not self.Constants.PLAYER_LOGO.is_file():
            restore_from_meipass(self.Constants.PLAYER_LOGO)
        if not self.Constants.STUDIO_LOGO.is_file():
            restore_from_meipass(self.Constants.STUDIO_LOGO)

        self.versioninfovariable: ctk.StringVar = ctk.StringVar(value="")
        info_label: ctk.CTkLabel = ctk.CTkLabel(self, textvariable=self.versioninfovariable, justify="left", font=ctk.CTkFont(size=13))
        info_label.place(x=20, y=10)

        logo: ctk.CTkLabel
        if mode == "Player":
            logo = ctk.CTkLabel(self, text="", image=load_image(self.Constants.PLAYER_LOGO, size=(122,122)))
        elif mode == "Studio":
            logo = ctk.CTkLabel(self, text="", image=load_image(self.Constants.STUDIO_LOGO, size=(122,122)))
        logo.place(x=(self.Constants.WIDTH // 2) - (122 // 2), y=56)

        self.textvariable: ctk.StringVar = ctk.StringVar(value="")
        label: ctk.CTkLabel = ctk.CTkLabel(self, textvariable=self.textvariable, width=self.Constants.WIDTH, font=ctk.CTkFont(size=14))
        label.place(x=0, y=203)

        progress_bar: ctk.CTkProgressBar = ctk.CTkProgressBar(self, mode="indeterminate", corner_radius=0, width=460, height=20)
        progress_bar.place(x=(self.Constants.WIDTH // 2) - (460 // 2), y=245)
        progress_bar.start()

        close_button = ctk.CTkButton(self, text="Cancel", width=130, height=34, corner_radius=2, command=self._on_cancel)
        close_button.place(x=(self.Constants.WIDTH // 2) - (130 // 2), y=273)
        
        self.geometry(self._get_geometry())


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