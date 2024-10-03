import os
import tkinter as tk
import customtkinter as ctk

from modules.filesystem import Directory
from modules.info import Project


class MainWindow:
    title: str = Project.NAME
    icon: str = os.path.join(Directory.program_files(), "resources", "favicon.ico")
    
    version: str = Project.VERSION

    width: int = 1100
    height: int = 600

    size: str = str(width)+"x"+str(height)

    navbar_width: int = 250
    section_width: int = width - navbar_width

    section_padding: int = 10

    background_navbar: str|tuple[str,str] = ("#f0f0f0", "#191919")
    background_main: str|tuple[str,str] = ("#f8f8f8", "#1c1c1c")
    background_subsection: str|tuple[str,str] = background_navbar

    theme: str = "blue"


    def __init__(self) -> None:
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme(self.theme)

        self.root: ctk.CTk = ctk.CTk()
        self.root.title(self.title)
        self.root.geometry(self.size)
        self.root.configure(fg_color=self.background_main)
        self.root.minsize(self.width, self.height)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        from . import navigation

        icon: str = self.icon
        if os.path.isfile(icon) and icon.endswith('.ico'):
            self.root.iconbitmap(icon)

        self.navbar = navigation.create(
            self.root,
            self.background_navbar,
            [
                {
                    "text": "Mods",
                    "icon": "mods",
                    "command": self.show_mods
                },
                {
                    "text": "Community Mods",
                    "icon": "marketplace",
                    "command": self.show_marketplace
                },
                {
                    "text": "FastFlags",
                    "icon": "fastflags",
                    "command": self.show_fastflags
                },
                {
                    "text": "Integrations",
                    "icon": "integrations",
                    "command": self.show_integrations
                },
                {
                    "text": "Settings",
                    "icon": "settings",
                    "command": self.show_settings
                },
                {
                    "text": "About",
                    "icon": "about",
                    "command": self.show_about
                }
            ],
            self.navbar_width,
            self.height
            )
        
        
        
        self.show_mods()

        self.root.mainloop()
    

    def show_mods(self) -> None:
        from .sections import mods
        mods.show(
            root=self.root,
            width=self.section_width,
            height=self.height,
            padx=self.section_padding,
            pady=self.section_padding
        )


    def show_marketplace(self) -> None:
        from .sections import marketplace
        marketplace.show(
            root=self.root,
            subsection_background=self.background_subsection,
            width=self.section_width,
            height=self.height,
            padx=self.section_padding,
            pady=self.section_padding
        )


    def show_fastflags(self) -> None:
        from .sections import fastflags
        fastflags.show(
            root=self.root,
            subsection_background=self.background_subsection,
            width=self.section_width,
            height=self.height,
            padx=self.section_padding,
            pady=self.section_padding
        )


    def show_integrations(self) -> None:
        from .sections import integrations
        integrations.show(
            root=self.root,
            subsection_background=self.background_subsection,
            width=self.section_width,
            height=self.height,
            padx=self.section_padding,
            pady=self.section_padding
        )


    def show_settings(self) -> None:
        from .sections import settings
        settings.show(
            root=self.root,
            subsection_background=self.background_subsection,
            width=self.section_width,
            height=self.height,
            padx=self.section_padding,
            pady=self.section_padding
        )


    def show_about(self) -> None:
        from .sections import about
        about.show(
            root=self.root,
            width=self.section_width,
            height=self.height,
            padx=self.section_padding,
            pady=self.section_padding
        )