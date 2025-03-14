from pathlib import Path
import json

from modules import Logger
from modules import exception_handler
from modules.info import ProjectData
from modules.config import special_settings
from modules.filesystem import Directory, restore_from_meipass
from modules.filesystem.exceptions import FileRestoreError

from .navigation import NavigationFrame
from .sections.mods import ModsSection
from .sections.marketplace import MarketplaceSection
from .sections.mod_generator import ModGeneratorSection
from .sections.fastflags import FastFlagsSection
from .sections.fastflag_configuration import FastFlagConfigurationSection
from .sections.global_basic_settings_editor import GlobalBasicSettingsSection
from .sections.launch_apps import LaunchAppsSection
from .sections.integrations import IntegrationsSection
from .sections.settings import SettingsSection
from .sections.about import AboutSection

from .popup_windows.font_import_window import FontImportWindow
from .popup_windows.mod_download_window import ModDownloadWindow
from .popup_windows.fastflag_preset_window import FastFlagPresetWindow

import customtkinter as ctk


class MainWindow(ctk.CTk):
    class Constants:
        WIDTH: int = 1100
        HEIGHT: int = 600
        FAVICON: Path = Directory.RESOURCES / "favicon.ico"


    class Sections:
        mods: ModsSection
        marketplace: MarketplaceSection
        mod_generator: ModGeneratorSection
        fastflags: FastFlagsSection
        fastflag_configuration: FastFlagConfigurationSection
        global_basic_settings: GlobalBasicSettingsSection
        launch_apps: LaunchAppsSection
        integrations: IntegrationsSection
        settings: SettingsSection
        about: AboutSection
    

    class PopupWindows:
        font_import_window: FontImportWindow
        mod_download_window: FontImportWindow
        fastflag_preset_window: FastFlagPresetWindow


    background_color: str | tuple[str, str] = "transparent"


    def __init__(self) -> None:
        selected_appearance: str = special_settings.get_value("appearance")
        ctk.set_appearance_mode(selected_appearance)
        
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
        ctk.set_default_color_theme(theme_file.resolve())

        super().__init__()
        self.title(ProjectData.NAME)
        self.resizable(False, False)
        if not self.Constants.FAVICON.is_file():
            restore_from_meipass(self.Constants.FAVICON)
        self.iconbitmap(self.Constants.FAVICON.resolve())

        try:
            with open(theme_file, "r") as file:
                data: dict[str, dict] = json.load(file)
            self.background_color = data["CTk"]["fg_color"]
        except Exception as e:
            Logger.error(f"Failed to load custom theme! {type(e).__name__}: {e}", prefix="MainWindow.__init__()")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(self, fg_color=self.background_color, width=self.Constants.WIDTH-NavigationFrame.Constants.WIDTH, height=self.Constants.HEIGHT, corner_radius=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=1, row=0, sticky="nsew", padx=(8,0), pady=4)

        self.PopupWindows.font_import_window = FontImportWindow(self)
        self.PopupWindows.mod_download_window = ModDownloadWindow(self)
        self.PopupWindows.fastflag_preset_window = FastFlagPresetWindow(self)

        self.Sections.mods = ModsSection(self, container, self.PopupWindows.font_import_window)
        self.Sections.marketplace = MarketplaceSection(self, container, self.PopupWindows.mod_download_window)
        self.Sections.mod_generator = ModGeneratorSection(self, container)
        self.Sections.fastflag_configuration = FastFlagConfigurationSection(self, container)
        self.Sections.fastflags = FastFlagsSection(self, container, self.Sections.fastflag_configuration, self.PopupWindows.fastflag_preset_window)
        self.Sections.global_basic_settings = GlobalBasicSettingsSection(self, container)
        self.Sections.launch_apps = LaunchAppsSection(self, container)
        self.Sections.integrations = IntegrationsSection(container)
        self.Sections.settings = SettingsSection(container)
        self.Sections.about = AboutSection(container)
        
        self.PopupWindows.font_import_window.set_refresh_function(self.Sections.mods.show)
        self.Sections.fastflag_configuration.set_return_command(self.Sections.fastflags.show)
        self.PopupWindows.fastflag_preset_window.set_refresh_function(self.Sections.fastflags.show)

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