from typing import Optional
from pathlib import Path

from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image
from modules.config import mods

from ..commands import add_mods, open_mods_folder

import customtkinter as ctk


class ModsSection:
    class Constants:
        SECTION_TITLE: str = "Mods"
        SECTION_DESCRIPTION: str = "Manage your mods"
    
    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont
        large_bold: ctk.CTkFont


    container: ctk.CTkScrollableFrame


    def __init__(self, container: ctk.CTkScrollableFrame) -> None:
        self.container = container
        self.Fonts.title = ctk.CTkFont(size=20, weight="bold")
        self.Fonts.large = ctk.CTkFont(size=16)
        self.Fonts.large_bold = ctk.CTkFont(size=16, weight="bold")


    def show(self) -> None:
        self._destroy()
        self._load_title()
        self._load_content()


    def _destroy(self) -> None:
        for widget in self.container.winfo_children():
            widget.destroy()


    def _load_title(self) -> None:
        frame: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(column=0, row=0, sticky="nsew", pady=(0,16), padx=(0,4))

        ctk.CTkLabel(frame, text=self.Constants.SECTION_TITLE, anchor="w", font=self.Fonts.title).grid(column=0, row=0, sticky="nsew")
        ctk.CTkLabel(frame, text=self.Constants.SECTION_DESCRIPTION, anchor="w", font=self.Fonts.large).grid(column=0, row=1, sticky="nsew")

        buttons: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
        buttons.grid(column=0, row=2, sticky="nsw", pady=(8,0))

        package_icon: Path = (Directory.RESOURCES / "menu" / "common" / "package").with_suffix(".png")
        if not package_icon.is_file():
            restore_from_meipass(package_icon)
        package_image = load_image(package_icon)

        folder_icon: Path = (Directory.RESOURCES / "menu" / "common" / "folder").with_suffix(".png")
        if not folder_icon.is_file():
            restore_from_meipass(folder_icon)
        folder_image = load_image(folder_icon)

        font_icon: Path = (Directory.RESOURCES / "menu" / "common" / "font").with_suffix(".png")
        if not font_icon.is_file():
            restore_from_meipass(font_icon)
        font_image = load_image(font_icon)

        ctk.CTkButton(buttons, text="Add mods", image=package_image, command=add_mods, width=1, anchor="w", compound=ctk.LEFT).grid(column=0, row=0, sticky="nsw")
        ctk.CTkButton(buttons, text="Open mods folder", image=folder_image, command=open_mods_folder, width=1, anchor="w", compound=ctk.LEFT).grid(column=1, row=0, sticky="nsw", padx=(8,0))
        ctk.CTkButton(buttons, text="Add font", image=font_image, command=None, width=1, anchor="w", compound=ctk.LEFT).grid(column=2, row=0, sticky="nsw", padx=(8,0))


    def _load_content(self) -> None:
        configured_mods: list[dict] = mods.read_file()

        container: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=0, row=1, sticky="nsew", padx=(0,4))

        if not Directory.MODS.is_dir():
            Directory.MODS.mkdir(parents=True, exist_ok=True)
            ctk.CTkLabel(container, text="No mods found!", anchor="w", font=self.Fonts.large_bold).grid(column=0, row=0, sticky="nsew")
            return

        all_mods: list[dict] = [
            mod for mod in configured_mods
            if (Directory.MODS / mod["name"]).is_dir()
        ] + [
            {
                "name": mod.name,
                "enabled": False,
                "priority": 0
            }
            for mod in Directory.MODS.iterdir()
            if mod.name not in [mod.get("name") for mod in configured_mods]
            or not mod.is_dir()
        ]

        if not all_mods:
            ctk.CTkLabel(container, text="No mods found!", anchor="w", font=self.Fonts.large_bold).grid(column=0, row=0, sticky="nsew")
            return

        bin_icon: Path = (Directory.RESOURCES / "menu" / "common" / "bin").with_suffix(".png")
        if not bin_icon.is_file():
            restore_from_meipass(bin_icon)
        bin_image = load_image(bin_icon)

        for i, mod in enumerate(all_mods):
            name: str = mod["name"]
            enabled: bool = mod["enabled"]
            priority: int = mod["priority"]
            
            frame: ctk.CTkFrame = ctk.CTkFrame(container)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid(column=0, row=i, sticky="nsew", pady=0 if i == 0 else (4,0))

            ctk.CTkButton(frame, image=bin_image, height=40, text="", command=None, width=1, anchor="w", compound=ctk.LEFT).grid(column=0, row=0, sticky="nsw", padx=4, pady=4)


        pass