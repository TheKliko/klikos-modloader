from pathlib import Path
import re

from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image

import customtkinter as ctk


class ModGeneratorSection:
    class Constants:
        SECTION_TITLE: str = "Mod Generator [BETA]"
        SECTION_DESCRIPTION: str = "This feature is still in development, expect things to break"
        SECTION_DISCLAIMER: str = "Disclaimer: this tool only generates the ImageSets, it does not generate a complete mod"
    
    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont
        bold: ctk.CTkFont


    root: ctk.CTk
    container: ctk.CTkScrollableFrame
    mod_name_entry: ctk.CTkEntry
    color_variable: ctk.StringVar


    def __init__(self, root: ctk.CTk, container: ctk.CTkScrollableFrame) -> None:
        self.root = root
        self.container = container
        self.Fonts.title = ctk.CTkFont(size=20, weight="bold")
        self.Fonts.large = ctk.CTkFont(size=16)
        self.Fonts.bold = ctk.CTkFont(weight="bold")


    def show(self) -> None:
        self._destroy()
        self._load_title()
        self._load_content()


    def _destroy(self) -> None:
        for widget in self.container.winfo_children():
            widget.destroy()


    # region title
    def _load_title(self) -> None:
        frame: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(column=0, row=0, sticky="nsew", pady=(0,16))

        ctk.CTkLabel(frame, text=self.Constants.SECTION_TITLE, anchor="w", font=self.Fonts.title).grid(column=0, row=0, sticky="nsew")
        ctk.CTkLabel(frame, text=self.Constants.SECTION_DISCLAIMER, anchor="w", font=self.Fonts.large).grid(column=0, row=1, sticky="nsew")
        ctk.CTkLabel(frame, text=self.Constants.SECTION_DESCRIPTION, anchor="w", font=self.Fonts.large).grid(column=0, row=2, sticky="nsew")
    # endregion


    # region content
    def _load_content(self) -> None:
        container: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=0, row=1, sticky="nsew", padx=(0,4))

        # name input
        name_frame: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
        name_frame.grid(column=0, row=0, sticky="nsew")
        ctk.CTkLabel(name_frame, text="Name:", anchor="w", font=self.Fonts.bold).grid(column=0, row=0, sticky="nw")
        self.mod_name_entry = ctk.CTkEntry(
            name_frame, width=256, height=40, validate="key",
            validatecommand=(self.root.register(lambda value: not re.search(r'[\\/:*?"<>|]', value)), "%P")
        )
        self.mod_name_entry.grid(column=0, row=1, sticky="nw")
        
        # color input
        color_frame: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
        color_frame.grid(column=0, row=1, sticky="nsew", pady=(16, 32))
        ctk.CTkLabel(color_frame, text="Color:", anchor="w", font=self.Fonts.bold).grid(column=0, row=0, sticky="w")

        self.color_visualizer = ctk.CTkFrame(color_frame, width=40, height=40)
        self.color_visualizer.grid(column=0, row=1, sticky="nw")
        
        self.color_variable = ctk.StringVar(value="None")
        ctk.CTkLabel(color_frame, textvariable=self.color_variable, anchor="w").grid(column=1, row=1, sticky="w", padx=(4, 8))
        
        color_select_icon: Path = (Directory.RESOURCES / "menu" / "common" / "color-select").with_suffix(".png")
        if not color_select_icon.is_file():
            restore_from_meipass(color_select_icon)
        color_select_image = load_image(color_select_icon)
        ctk.CTkButton(color_frame, text="Select color", image=color_select_image, command=self._select_color, width=1, anchor="w", compound=ctk.LEFT).grid(column=2, row=1, sticky="w")

        # Run button
        run_icon: Path = (Directory.RESOURCES / "menu" / "common" / "run").with_suffix(".png")
        if not run_icon.is_file():
            restore_from_meipass(run_icon)
        run_image = load_image(run_icon)
        ctk.CTkButton(container, text="Generate mod", image=run_image, command=self._run, width=1, anchor="w", compound=ctk.LEFT).grid(column=0, row=2, sticky="nsw")
    # endregion


    # region functions
    def _select_color(self) -> None:
        pass

    def _run(self) -> None:
        pass
    # endregion