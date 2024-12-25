from pathlib import Path
import json

from modules import Logger
from modules import exception_handler
from modules.info import ProjectData
from modules.filesystem import Directory, restore_from_meipass

from .navigation import NavigationFrame
from .sections.mods import ModsSection
from .sections.marketplace import MarketplaceSection
from .sections.mod_generator import ModGeneratorSection
from .sections.fastflags import FastFlagsSection
from .sections.launch_apps import LaunchAppsSection
from .sections.integrations import IntegrationsSection
from .sections.settings import SettingsSection
from .sections.about import AboutSection

import customtkinter as ctk


class MainWindow(ctk.CTk):
    class Constants:
        WIDTH: int = 1100
        HEIGHT: int = 600
        THEME: Path = Directory.RESOURCES / "theme.json"
        FAVICON: Path = Directory.RESOURCES / "favicon.ico"


    class Sections:
        mods: ModsSection
        marketplace: MarketplaceSection
        mod_generator: ModGeneratorSection
        fastflags: FastFlagsSection
        launch_apps: LaunchAppsSection
        integrations: IntegrationsSection
        settings: SettingsSection
        about: AboutSection


    background_color: str | tuple[str, str] = "transparent"


    def __init__(self) -> None:
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

        try:
            with open(self.Constants.THEME, "r") as file:
                data: dict[str, dict] = json.load(file)
            self.background_color = data["CTk"]["fg_color"]
        except Exception as e:
            Logger.error(f"Failed to load custom theme! {type(e).__name__}: {e}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(self, fg_color=self.background_color, width=self.Constants.WIDTH-NavigationFrame.Constants.WIDTH, height=self.Constants.HEIGHT, corner_radius=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=1, row=0, sticky="nsew", padx=(8,0), pady=4)
        self.Sections.mods = ModsSection(self, container)
        self.Sections.marketplace = MarketplaceSection(container)
        self.Sections.mod_generator = ModGeneratorSection(container)
        self.Sections.fastflags = FastFlagsSection(container)
        self.Sections.launch_apps = LaunchAppsSection(container)
        self.Sections.integrations = IntegrationsSection(container)
        self.Sections.settings = SettingsSection(container)
        self.Sections.about = AboutSection(container)

        self.navigation: NavigationFrame = NavigationFrame(self)
        self.navigation.grid(column=0, row=0, sticky="nsew")

        self.bind_all("<Button-1>", lambda event: self._set_widget_focus(event))
        self.report_callback_exception = self._on_error
        self.geometry(self._get_geometry())

        # Default
        self.Sections.mods.show()
    

    def _set_widget_focus(self, event) -> None:
        if not hasattr(event, "widget"):
            return
        if not hasattr(event.widget, "focus_set"):
            return
        event.widget.focus_set()


    def _get_geometry(self) -> str:
        x: int = (self.winfo_screenwidth() // 2) - (self.Constants.WIDTH // 2)
        y: int = (self.winfo_screenheight() // 2) - (self.Constants.HEIGHT // 2)
        return f"{self.Constants.WIDTH}x{self.Constants.HEIGHT}+{x}+{y}"
    

    def _on_close(self, *args, **kwargs) -> None:
        self.after(1, self.destroy)
    

    def _on_error(self, exception_class, exception, traceback) -> None:
        exception_handler.run(exception)
        self._on_close()