from pathlib import Path
from typing import Callable
import json

from modules import Logger
from modules.config import special_settings
from modules.info import ProjectData
from modules.filesystem import Directory, restore_from_meipass
from modules.filesystem.exceptions import FileRestoreError
from modules.functions.interface.image import load as load_image

from .commands import launch_roblox_player, launch_roblox_studio

import customtkinter as ctk


class NavigationFrame(ctk.CTkFrame):
    class Constants:
        WIDTH: int = 250
        PADDING: int = 16
        ICON_SIZE: tuple[int, int] = (20, 20)
        BUTTON_HEIGHT: int = 36
        FONT_SIZE: int = 14

        HEADER_LOGO_LIGHT: Path = Directory.RESOURCES / "menu" / "navigation" / "light" / "logo.png"
        HEADER_LOGO_DARK: Path = Directory.RESOURCES / "menu" / "navigation" / "dark" / "logo.png"

        FOOTER_LOGO_PLAYER: Path = Directory.RESOURCES / "launcher" / "player.png"
        FOOTER_LOGO_STUDIO: Path = Directory.RESOURCES / "launcher" / "studio.png"
        FOOTER_LOGO_SIZE: tuple[int, int] = (20, 20)
        FOOTER_BUTTON_COLOR: str | tuple[str, str] = "#02b758"
        FOOTER_BUTTON_HOVER_COLOR: str | tuple[str, str] = ("#01833f", "#02dd6a")

        SECTIONS: list[dict[str, str | Callable | dict[str, Path]]] = [
            {
                "name": "Mods",
                "icon": {
                    "light": Directory.RESOURCES / "menu" / "navigation" / "light" / "mods.png",
                    "dark": Directory.RESOURCES / "menu" / "navigation" / "dark" / "mods.png"
                }
            },
            {
                "name": "Community Mods",
                "icon": {
                    "light": Directory.RESOURCES / "menu" / "navigation" / "light" / "marketplace.png",
                    "dark": Directory.RESOURCES / "menu" / "navigation" / "dark" / "marketplace.png"
                }
            },
            {
                "name": "Mod Generator",
                "icon": {
                    "light": Directory.RESOURCES / "menu" / "navigation" / "light" / "mod-creator.png",
                    "dark": Directory.RESOURCES / "menu" / "navigation" / "dark" / "mod-creator.png"
                }
            },
            {
                "name": "FastFlags",
                "icon": {
                    "light": Directory.RESOURCES / "menu" / "navigation" / "light" / "fastflags.png",
                    "dark": Directory.RESOURCES / "menu" / "navigation" / "dark" / "fastflags.png"
                }
            },
            {
                "name": "GlobalBasicSettings",
                "icon": {
                    "light": Directory.RESOURCES / "menu" / "navigation" / "light" / "global-basic-settings.png",
                    "dark": Directory.RESOURCES / "menu" / "navigation" / "dark" / "global-basic-settings.png"
                }
            },
            {
                "name": "Launch Apps",
                "icon": {
                    "light": Directory.RESOURCES / "menu" / "navigation" / "light" / "launch-integrations.png",
                    "dark": Directory.RESOURCES / "menu" / "navigation" / "dark" / "launch-integrations.png"
                }
            },
            {
                "name": "Integrations",
                "icon": {
                    "light": Directory.RESOURCES / "menu" / "navigation" / "light" / "integrations.png",
                    "dark": Directory.RESOURCES / "menu" / "navigation" / "dark" / "integrations.png"
                }
            },
            {
                "name": "Settings",
                "icon": {
                    "light": Directory.RESOURCES / "menu" / "navigation" / "light" / "settings.png",
                    "dark": Directory.RESOURCES / "menu" / "navigation" / "dark" / "settings.png"
                }
            },
            {
                "name": "About",
                "icon": {
                    "light": Directory.RESOURCES / "menu" / "navigation" / "light" / "about.png",
                    "dark": Directory.RESOURCES / "menu" / "navigation" / "dark" / "about.png"
                }
            }
        ]
    

    class Colors:
        main_fg_color: str | tuple[str, str] = ("#fbfbfb", "#202020")
        main_text_color: str | tuple[str, str] = ("gray14", "gray84")
        button_fg_color: str | tuple[str, str] = "transparent"
        button_hover_color: str | tuple[str, str] = ("#eaeaea", "#2d2d2d")
        button_text_color: str | tuple[str, str] = ("#000", "#DCE4EE")


    header: ctk.CTkFrame
    buttons: ctk.CTkFrame
    footer: ctk.CTkFrame


    def __init__(self, root) -> None:
        # Load NavigationFrame theme
        try:
            selected_theme: str = special_settings.get_value("theme")
            theme_file: Path = Directory.THEMES / f"{selected_theme}.json"
            if not theme_file.is_file() and selected_theme != "default":
                try:
                    restore_from_meipass(theme_file)
                except FileRestoreError:
                    Logger.info("Theme file not found, reverting to default theme!", prefix="NavigationFrame.__init__()")
                    special_settings.set_value("theme", "default")
                    theme_file = Directory.THEMES / "default.json"
            if not theme_file.is_file():
                restore_from_meipass(theme_file)
            with open(theme_file, "r") as file:
                theme_data: dict = json.load(file)
            navigation_frame: dict[str, dict[str, str | list[str]]] | None = theme_data.get("NavigationFrame")
            if navigation_frame:
                main_data: dict[str, str | list[str]] = navigation_frame.get("main", {})
                button_data: dict[str, str | list[str]] = navigation_frame.get("buttons", {})

                main_fg_color: str | tuple[str, str] | None = self._get_color(main_data, "fg_color")
                main_text_color: str | tuple[str, str] | None = self._get_color(main_data, "text_color")
                button_fg_color: str | tuple[str, str] | None = self._get_color(button_data, "fg_color")
                button_text_color: str | tuple[str, str] | None = self._get_color(button_data, "text_color")
                button_hover_color: str | tuple[str, str] | None = self._get_color(button_data, "hover_color")

                if main_fg_color:
                    self.Colors.main_fg_color = main_fg_color
                if main_text_color:
                    self.Colors.main_text_color = main_text_color
                if button_fg_color:
                    self.Colors.button_fg_color = button_fg_color
                if button_text_color:
                    self.Colors.button_text_color = button_text_color
                if button_hover_color:
                    self.Colors.button_hover_color = button_hover_color

        except Exception as e:
            Logger.warning(f"Failed to load NavigationFrame theme! {type(e).__name__}: {e}", prefix="NavigationFrame.__init__()")
        
        
        super().__init__(root, width=self.Constants.WIDTH, corner_radius=0, fg_color=self.Colors.main_fg_color)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        

        self.header = self._create_header_frame()
        self.header.grid(column=0, row=0, padx=self.Constants.PADDING, pady=self.Constants.PADDING, sticky="nsew")

        self.buttons = self._create_buttons_frame(root)
        self.buttons.grid(column=0, row=1, padx=self.Constants.PADDING, sticky="nsew")

        self.footer = self._create_footer_frame()
        self.footer.grid(column=0, row=2, padx=self.Constants.PADDING, pady=self.Constants.PADDING, sticky="sw")
    

    def _get_color(self, data: dict[str, str | list[str]], attribute: str) -> str | tuple[str, str] | None:
        value: str | list[str] | None = data.get(attribute)
        if isinstance(value, list) and len(value) == 2:
            return (value[0], value[1])
        if isinstance(value, str):
            return value
        return None


    def _create_button(self, master, text: str, image, command: Callable) -> ctk.CTkButton:
        width: int = self.Constants.WIDTH - 2 * self.Constants.PADDING
        height: int = 36

        return ctk.CTkButton(master, text=text, image=image, command=command, width=width, height=height, fg_color=self.Colors.button_fg_color, hover_color=self.Colors.button_hover_color, text_color=self.Colors.button_text_color, compound="left", anchor="w", corner_radius=4)
    
    
    def _create_header_frame(self) -> ctk.CTkFrame:
        if not self.Constants.HEADER_LOGO_LIGHT.is_file():
            restore_from_meipass(self.Constants.HEADER_LOGO_LIGHT)
        if not self.Constants.HEADER_LOGO_DARK.is_file():
            restore_from_meipass(self.Constants.HEADER_LOGO_DARK)

        frame: ctk.CTkFrame = ctk.CTkFrame(self, width=self.Constants.WIDTH - 2 * self.Constants.PADDING, height=64, fg_color="transparent")
        
        logo: ctk.CTkLabel = ctk.CTkLabel(frame, text="", image=load_image(light=self.Constants.HEADER_LOGO_LIGHT, dark=self.Constants.HEADER_LOGO_DARK, size=(64, 64)), fg_color="transparent")
        logo.grid(column=0, row=0, rowspan=2, sticky="w", padx=(0,8))

        container: ctk.CTkFrame = ctk.CTkFrame(frame, height=64, fg_color="transparent")
        container.grid(column=1, row=0, sticky="w")

        name: ctk.CTkLabel = ctk.CTkLabel(container, font=ctk.CTkFont(weight="bold"), text=ProjectData.NAME, justify="left", fg_color="transparent", text_color=self.Colors.main_text_color)
        name.pack(anchor="w")

        version: ctk.CTkLabel = ctk.CTkLabel(container, font=ctk.CTkFont(size=12), text=f"Version {ProjectData.VERSION}", justify="left", fg_color="transparent", text_color=self.Colors.main_text_color)
        version.pack(anchor="w", pady=0)

        return frame


    def _create_buttons_frame(self, root) -> ctk.CTkFrame:
        width: int = self.Constants.WIDTH - 2 * self.Constants.PADDING
        icon_size: tuple[int, int] = (20, 20)
        frame: ctk.CTkFrame = ctk.CTkFrame(self, width=width, fg_color="transparent")

        for i, section in enumerate(self.Constants.SECTIONS):
            name: str = section["name"]
            light_icon: Path = section["icon"]["light"]
            dark_icon: Path = section["icon"]["dark"]
            command: Callable = None

            if not light_icon.is_file():
                restore_from_meipass(light_icon)
            if not dark_icon.is_file():
                restore_from_meipass(dark_icon)
            image = load_image(light_icon, dark_icon, size=icon_size)

            # idk ¯\_(ツ)_/¯
            match name.lower():
                case "mods":
                    command = root.Sections.mods.show
                case "community mods":
                    command = root.Sections.marketplace.show
                case "mod generator":
                    command = root.Sections.mod_generator.show
                case "fastflags":
                    command = root.Sections.fastflags.show
                case "globalbasicsettings":
                    command = root.Sections.global_basic_settings.show
                case "launch apps":
                    command = root.Sections.launch_apps.show
                case "integrations":
                    command = root.Sections.integrations.show
                case "settings":
                    command = root.Sections.settings.show
                case "about":
                    command = root.Sections.about.show

            button: ctk.CTkButton = self._create_button(master=frame, text=name, command=command, image=image)
            button.grid(column=0, row=i, pady=0 if i == 0 else (4,0))

        return frame


    def _create_footer_frame(self) -> ctk.CTkFrame:
        if not self.Constants.FOOTER_LOGO_PLAYER.is_file():
            restore_from_meipass(self.Constants.FOOTER_LOGO_PLAYER)
        if not self.Constants.FOOTER_LOGO_STUDIO.is_file():
            restore_from_meipass(self.Constants.FOOTER_LOGO_STUDIO)

        width: int = self.Constants.WIDTH - 2 * self.Constants.PADDING
        button_width: int = width
        button_height: int = 36

        frame: ctk.CTkFrame = ctk.CTkFrame(self, width=width, height=button_height * 2 + 4, fg_color="transparent")
        frame.grid_propagate(False)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        player: ctk.CTkButton = self._create_button(master=frame, text="Launch Roblox Player", command=launch_roblox_player, image=load_image(self.Constants.FOOTER_LOGO_PLAYER, size=self.Constants.FOOTER_LOGO_SIZE))
        # ctk.CTkButton(frame, width=button_width, height=button_height, text="Launch Roblox Player", image=load_image(self.Constants.FOOTER_LOGO_PLAYER, size=self.Constants.FOOTER_LOGO_SIZE), compound="left", anchor="w", fg_color="transparent", text_color=("#000","#DCE4EE"), hover_color=("#eaeaea", "#2d2d2d"), command=launch_roblox_player)
        player.grid(column=0, row=0, sticky="n")

        studio: ctk.CTkButton = self._create_button(master=frame, text="Launch Roblox Studio", command=launch_roblox_studio, image=load_image(self.Constants.FOOTER_LOGO_STUDIO, size=self.Constants.FOOTER_LOGO_SIZE))
        # ctk.CTkButton(frame, width=button_width, height=button_height, text="Launch Roblox Studio", image=load_image(self.Constants.FOOTER_LOGO_STUDIO, size=self.Constants.FOOTER_LOGO_SIZE), compound="left", anchor="w", fg_color="transparent", text_color=("#000","#DCE4EE"), hover_color=("#eaeaea", "#2d2d2d"), command=launch_roblox_studio)
        studio.grid(column=0, row=1, sticky="s")

        return frame