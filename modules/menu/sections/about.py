import webbrowser
from pathlib import Path

from modules.info import ProjectData, Help, LICENSES
from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image

import customtkinter as ctk


class AboutSection:
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
        self._load_content()


    def _destroy(self) -> None:
        for widget in self.container.winfo_children():
            widget.destroy()


    # region title
    def _load_title(self) -> None:
        frame: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(column=0, row=0, sticky="nsew", pady=(0,24))

        # Banner
        banner_file: Path = (Directory.RESOURCES / "menu" / "about" / "banner").with_suffix(".png")
        if not banner_file.is_file():
            restore_from_meipass(banner_file)
        banner_image = load_image(banner_file, size=(548, 165))

        ctk.CTkLabel(frame, text="", image=banner_image).grid(column=0, row=0, sticky="new")

        # Buttons
        buttons: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
        buttons.grid(column=0, row=2, sticky="nsew")
        buttons.grid_columnconfigure(0, weight=1)
        buttons.grid_columnconfigure(4, weight=1)

        github_icon: Path = (Directory.RESOURCES / "menu" / "about" / "github").with_suffix(".png")
        if not github_icon.is_file():
            restore_from_meipass(github_icon)
        github_image = load_image(github_icon)

        chat_icon: Path = (Directory.RESOURCES / "menu" / "about" / "chat").with_suffix(".png")
        if not chat_icon.is_file():
            restore_from_meipass(chat_icon)
        chat_image = load_image(chat_icon)

        ctk.CTkButton(buttons, text="View on GitHub", image=github_image, command=lambda: webbrowser.open_new_tab(Help.GITHUB), width=1, anchor="w", compound=ctk.LEFT).grid(column=1, row=0, sticky="nsew")
        ctk.CTkButton(buttons, text="Changelog", image=github_image, command=lambda: webbrowser.open_new_tab(Help.RELEASES), width=1, anchor="w", compound=ctk.LEFT).grid(column=2, row=0, sticky="nsew", padx=(8,0))
        ctk.CTkButton(buttons, text="Join our Discord", image=chat_image, command=lambda: webbrowser.open_new_tab(Help.DISCORD), width=1, anchor="w", compound=ctk.LEFT).grid(column=3, row=0, sticky="nsew", padx=(8,0))
    # endregion

    
    # region content
    def _load_content(self) -> None:
        container: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=0, row=1, sticky="nsew", padx=(0,4))

        # 268 8 269 8 268
        # Licenses
        licenses_container: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
        licenses_container.grid(column=0, row=0, sticky="nsew", pady=(0, 24))
        ctk.CTkLabel(licenses_container, text="Licenses", font=self.Fonts.title, anchor="w").grid(column=0, row=0, columnspan=3, sticky="ew")

        for i, license in enumerate(LICENSES):
            license_frame: ctk.CTkFrame = ctk.CTkFrame(licenses_container)
            license_frame.grid(column=self._get_license_column(), row=self._get_license_row(), sticky="nsew")
    # endregion


    # region functions
    def _get_license_column() -> int:
        return
    
    
    def _get_license_row() -> int:
        return
    # endregion