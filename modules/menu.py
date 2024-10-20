import os
import sys
import shutil
from typing import Callable, Literal

from modules.logger import logger
from modules.info import ProjectData
from modules.filesystem import Directory, logged_path
from modules.interface.images import load_image

import customtkinter as ctk


IS_FROZEN = getattr(sys, "frozen", False)

icon_path_extension: str = os.path.join("resources", "favicon.ico")
icon_path: str | None = os.path.join(Directory.root(), icon_path_extension)
if not os.path.isfile(icon_path):
    if IS_FROZEN:
        icon_path = os.path.join(Directory._MEI(), icon_path_extension)
    else:
        icon_path = None

theme_path_extension: str = os.path.join("resources", "theme.json")
theme_path: str = os.path.join(Directory.root(), theme_path_extension)
if not os.path.isfile(theme_path):
    if IS_FROZEN:
        os.makedirs(os.path.dirname(theme_path), exist_ok=True)
        shutil.copy(os.path.join(Directory._MEI(), "resources", "theme.json"), theme_path)
        logger.warning(f"File restored from _MEI: {logged_path.get(theme_path)}")
        theme_path = os.path.join(Directory._MEI(), theme_path_extension)
    else:
        theme_path = "blue"


class MainWindow:
    root: ctk.CTk

    width: int = 1100
    height: int = 600
    size: str = f"{width}x{height}"

    title: str = "Modloader Menu"
    icon: str = icon_path
    theme: str = theme_path
    appearance: str = "System"

    navigation: ctk.CTkFrame
    navigation_width: int = 250
    navigation_icon_size: tuple[int, int] = (24, 24)
    navigation_button_hover_background: str | tuple[str, str] = ("#eaeaea", "#2d2d2d")
    navigation_buttons: list[dict[str, str | Callable | None]] = [
        {
            "text": "Mods",
            "icon": "mods.png",
            "command": None
        },
        {
            "text": "Community Mods",
            "icon": "marketplace.png",
            "command": None
        },
        {
            "text": "FastFlags",
            "icon": "fastflags.png",
            "command": None
        },
        {
            "text": "Integrations",
            "icon": "integrations.png",
            "command": None
        },
        {
            "text": "Settings",
            "icon": "settings.png",
            "command": None
        },
        {
            "text": "About",
            "icon": "about.png",
            "command": None
        }
    ]





    def __init__(self) -> None:
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

        if self.icon is not None:
            self.root.iconbitmap(self.icon)
        
        ctk.CTkLabel(
            self.root,
            text="Modloader menu!",
            font=ctk.CTkFont(weight="bold", size=16)
        ).grid(column=1, row=0, sticky="nsew")

        self._create_navigation()
    

    def show(self) -> None:
        self.root.mainloop()
    




    def _create_navigation(self) -> None:
        from modules.interface import fonts
        def create_header() -> None:
            header: ctk.CTkFrame = ctk.CTkFrame(
                self.navigation,
                width=self.navigation_width,
                height=80,
                fg_color="transparent"
            )
            header.grid_columnconfigure(0, weight=1)
            header.grid_rowconfigure(1, weight=1)
            header.grid(column=0, row=0, sticky="nsew", pady=24)

            logo_base_path: str = os.path.join(Directory.root(), "resources", "menu", "logo")
            light_icon_path: str = os.path.join(logo_base_path, "light.png")
            dark_icon_path: str = os.path.join(logo_base_path, "dark.png")
            if not os.path.isfile(light_icon_path) and IS_FROZEN:
                os.makedirs(logo_base_path, exist_ok=True)
                shutil.copy(os.path.join(Directory._MEI(), "resources", "menu", "logo", "light.png"), logo_base_path)
                logger.warning(f"File restored from _MEI: {logged_path.get(light_icon_path)}")
            if not os.path.isfile(dark_icon_path) and IS_FROZEN:
                os.makedirs(logo_base_path, exist_ok=True)
                shutil.copy(os.path.join(Directory._MEI(), "resources", "menu", "logo", "dark.png"), logo_base_path)
                logger.warning(f"File restored from _MEI: {logged_path.get(dark_icon_path)}")
                
            ctk.CTkLabel(
                header,
                text=None,
                image=load_image(
                    light=light_icon_path,
                    dark=dark_icon_path,
                    size=(64,64)
                ),
                anchor="center",
                justify="center"
            ).grid(column=0, row=0, sticky="nsew")
    
            ctk.CTkLabel(
                header,
                text=ProjectData.NAME,
                anchor="center",
                justify="center",
                font=fonts.SUBTITLE
            ).grid(column=0, row=1, sticky="nsew", pady=(8,0))

            ctk.CTkLabel(
                header,
                text="Version "+ProjectData.VERSION,
                anchor="center",
                justify="center",
                font=fonts.SMALL_BOLD
            ).grid(column=0, row=2, sticky="nsew")


        def create_buttons() -> None:
            button_frame: ctk.CTkFrame = ctk.CTkFrame(
                self.navigation,
                width=self.navigation_width,
                fg_color="transparent"
            )
            button_frame.grid_columnconfigure(0, weight=1)
            button_frame.grid(column=0, row=1, sticky="nsew")
            for i, button in enumerate(self.navigation_buttons):
                icon: str = button.get("icon", "") or ""

                if icon:
                    directory_path_light: str = os.path.join(Directory.root(), "resources", "menu", "navigation", "light")
                    directory_path_dark: str = os.path.join(Directory.root(), "resources", "menu", "navigation", "dark")
                    icon_path_light: str = os.path.join(directory_path_light, icon)
                    icon_path_dark: str = os.path.join(directory_path_dark, icon)
                    if not os.path.isfile(icon_path_light) and IS_FROZEN:
                        os.makedirs(directory_path_light, exist_ok=True)
                        shutil.copy(os.path.join(Directory._MEI(), "resources", "menu", "navigation", "light", icon), directory_path_light)
                        logger.warning(f"File restored from _MEI: {logged_path.get(icon_path_light)}")
                    if not os.path.isfile(icon_path_dark) and IS_FROZEN:
                        os.makedirs(directory_path_dark, exist_ok=True)
                        shutil.copy(os.path.join(Directory._MEI(), "resources", "menu", "navigation", "dark", icon), directory_path_dark)
                        logger.warning(f"File restored from _MEI: {logged_path.get(icon_path_dark)}")
                    image = load_image(
                        light=icon_path_light,
                        dark=icon_path_dark,
                        size=self.navigation_icon_size
                    )
                else:
                    image = ""
                
                command: Callable | Literal[""] = button.get("command", "") or ""
                text: str = button.get("text", "") or ""
                
                ctk.CTkButton(
                    button_frame,
                    text=text,
                    command=command,
                    image=image,
                    compound=ctk.LEFT,
                    anchor="w",
                    font=fonts.NAVIGATION,
                    fg_color="transparent",
                    hover_color=self.navigation_button_hover_background,
                    text_color=("#000","#DCE4EE")
                ).grid(
                    column=0,
                    row=i,
                    sticky="nsew",
                    padx=10,
                    pady=10 if i == 0 else (0, 10)
                )



        frame: ctk.CTkFrame = ctk.CTkFrame(
            self.root,
            width=self.navigation_width
        )
        frame.grid_propagate(False)
        frame.grid(column=0,row=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        self.navigation = frame

        create_header()
        create_buttons()