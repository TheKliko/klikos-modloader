from pathlib import Path

from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image
from modules.config import settings

import customtkinter as ctk


class SettingsSection:
    class Constants:
        SECTION_TITLE: str = "Settings"
        SECTION_DESCRIPTION: str = "Manage your settings"
        ENTRY_INNER_PADDING: int = 0
        ENTRY_OUTER_PADDING: int = 8
        ENTRY_GAP: int = 8
    
    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont
        bold: ctk.CTkFont


    container: ctk.CTkScrollableFrame


    def __init__(self, container: ctk.CTkScrollableFrame) -> None:
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
        ctk.CTkLabel(frame, text=self.Constants.SECTION_DESCRIPTION, anchor="w", font=self.Fonts.large).grid(column=0, row=1, sticky="nsew")

        buttons: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
        buttons.grid(column=0, row=2, sticky="nsw", pady=(8,0))

        restore_icon: Path = (Directory.RESOURCES / "menu" / "common" / "restore").with_suffix(".png")
        if not restore_icon.is_file():
            restore_from_meipass(restore_icon)
        restore_image = load_image(restore_icon)

        ctk.CTkButton(buttons, text="Reset to default", image=restore_image, command=settings.reset_all, width=1, anchor="w", compound=ctk.LEFT).grid(column=0, row=0, sticky="nsw")
    # endregion


    # region content
    def _load_content(self) -> None:
        items: dict[str, dict] = settings.read_file()

        container: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=0, row=1, sticky="nsew", padx=(0,4))

        for i, (key, item) in enumerate(items.items()):
            try:
                name: str = item["name"]
                description: str = item["description"]
                value: bool = item["value"]
            except KeyError:
                continue

            frame: ctk.CTkFrame = ctk.CTkFrame(container)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid(column=0, row=i, sticky="nsew", pady=0 if i == 0 else (self.Constants.ENTRY_GAP,0))

            # Name label
            name_frame: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
            name_frame.grid_columnconfigure(0, weight=1)
            name_frame.grid(column=0, row=0, sticky="new", padx=(self.Constants.ENTRY_OUTER_PADDING, self.Constants.ENTRY_INNER_PADDING), pady=self.Constants.ENTRY_OUTER_PADDING)

            ctk.CTkLabel(name_frame, text=name, anchor="w", font=self.Fonts.bold).grid(column=0, row=0, sticky="nw")
            ctk.CTkLabel(name_frame, text=description, anchor="w").grid(column=0, row=1, sticky="nw")

            # Toggle
            var: ctk.BooleanVar = ctk.BooleanVar(value=value)
            ctk.CTkSwitch(
                frame, text="", width=48, variable=var, onvalue=True, offvalue=False,
                command=lambda key=key, var=var: settings.set_value(key, var.get())
            ).grid(column=1, row=0, sticky="e", padx=(self.Constants.ENTRY_INNER_PADDING, self.Constants.ENTRY_OUTER_PADDING), pady=self.Constants.ENTRY_OUTER_PADDING)
    # endregion
    

    # region functions
    def _toggle_setting(self, key: str, value: bool) -> None:
        print(key)
        print(value)
    # endregion