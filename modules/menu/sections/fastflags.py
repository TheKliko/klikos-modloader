from pathlib import Path

from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image

from ..commands import add_mods, open_mods_folder

import customtkinter as ctk


class FastFlagsSection:
    class Constants:
        SECTION_TITLE: str = "FastFlags"
        SECTION_DESCRIPTION: str = "Manage your FastFlags"
    
    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont


    container: ctk.CTkScrollableFrame


    def __init__(self, container: ctk.CTkScrollableFrame) -> None:
        self.container = container
        self.Fonts.title = ctk.CTkFont(size=20, weight="bold")
        self.Fonts.large = ctk.CTkFont(size=16)


    def show(self) -> None:
        self._destroy()
        self._load_title()


    def _destroy(self) -> None:
        for widget in self.container.winfo_children():
            widget.destroy()


    def _load_title(self) -> None:
        frame: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(column=0, row=0, sticky="nsew", pady=(0,16))

        ctk.CTkLabel(frame, text=self.Constants.SECTION_TITLE, anchor="w", font=self.Fonts.title).grid(column=0, row=0, sticky="nsew")
        ctk.CTkLabel(frame, text=self.Constants.SECTION_DESCRIPTION, anchor="w", font=self.Fonts.large).grid(column=0, row=1, sticky="nsew")

        buttons: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
        buttons.grid(column=0, row=2, sticky="nsw", pady=(8,0))

        package_icon: Path = (Directory.RESOURCES / "menu" / "common" / "package").with_suffix(".png")
        folder_icon: Path = (Directory.RESOURCES / "menu" / "common" / "folder").with_suffix(".png")

        if not package_icon.is_file():
            restore_from_meipass(package_icon)
        if not folder_icon.is_file():
            restore_from_meipass(folder_icon)
        
        package_image = load_image(package_icon)
        folder_image = load_image(folder_icon)

        ctk.CTkButton(buttons, text="New profile", image=package_image, command=None, width=1, anchor="w", compound=ctk.LEFT).grid(column=0, row=0, sticky="nsw")
        ctk.CTkButton(buttons, text="Presets", image=folder_image, command=None, width=1, anchor="w", compound=ctk.LEFT).grid(column=1, row=0, sticky="nsw", padx=(8,0))