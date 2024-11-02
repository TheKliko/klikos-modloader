import os
import sys
import json
import threading
import traceback
from typing import Callable, Literal
import webbrowser

from modules import error_handler
from modules.logger import logger
from modules.info import ProjectData, Hyperlink, LICENSES
from modules.filesystem import Directory
from modules.interface.images import load_image, load_image_from_url
from modules.functions.restore_from_mei import restore_from_mei, FileRestoreError
from modules.functions.config import settings
from modules.functions.get_latest_version import get_latest_version
from modules.functions.marketplace_mod_download import marketplace_mod_download
from modules import request
from modules.request import GitHubApi, Response
from modules import bloxstrap_mode

from tkinter import filedialog, messagebox
import customtkinter as ctk


IS_FROZEN = getattr(sys, "frozen", False)

icon_path_extension: str = os.path.join("resources", "favicon.ico")
icon_path: str | None = os.path.join(Directory.root(), icon_path_extension)
if isinstance(icon_path, str):
    if not os.path.isfile(icon_path):
        if IS_FROZEN:
            restore_from_mei(icon_path)
        else:
            icon_path = None

theme_path_extension: str = os.path.join("resources", "theme.json")
theme_path: str = os.path.join(Directory.root(), theme_path_extension)
if not os.path.isfile(theme_path):
    try:
        restore_from_mei(theme_path)
    except Exception as e:
        theme_path = "blue"


# region MainWindow
class MainWindow:
    root: ctk.CTk

    width: int = 1100
    height: int = 600
    size: str = f"{width}x{height}"

    title: str = ProjectData.NAME
    icon: str | None = icon_path
    theme: str = theme_path
    appearance: str = "System"

    navigation: ctk.CTkFrame
    navigation_width: int = 250
    navigation_icon_size: tuple[int, int] = (24, 24)
    navigation_button_hover_background: str | tuple[str, str] = ("#eaeaea", "#2d2d2d")
    navigation_buttons: list[dict[str, str | Callable | None]]

    active_section: str = ""
    content: ctk.CTkScrollableFrame

    font_bold: ctk.CTkFont
    font_title: ctk.CTkFont
    font_subtitle: ctk.CTkFont
    font_small: ctk.CTkFont
    font_small_bold: ctk.CTkFont
    font_13: ctk.CTkFont
    font_13_bold: ctk.CTkFont
    font_navigation: ctk.CTkFont
    font_medium_bold: ctk.CTkFont
    font_large: ctk.CTkFont
    font_large_italic: ctk.CTkFont
    font_large_bold: ctk.CTkFont

    mod_thumbnail_size: tuple[int, int] = (64,64)


    #region __init__()
    def __init__(self) -> None:
        ctk.set_appearance_mode(self.appearance)
        try:
            ctk.set_default_color_theme(self.theme)
        except Exception as e:
            logger.error(f"Bad theme file! {type(e).__name__}: {e}")
            logger.warning("Using default theme...")
            if IS_FROZEN:
                ctk.set_default_color_theme(os.path.join(Directory._MEI(), "resources", "theme.json"))
            else:
                ctk.set_default_color_theme("blue")
            messagebox.showwarning(ProjectData.NAME, "Bad theme file!\nReverted to default theme")
        
        if os.path.isfile(theme_path):
            try:
                with open(self.theme, "r") as file:
                    data: dict[str, dict] = json.load(file)
                self.root_background = data.get("CTk", {}).get("fg_color", "transparent")
            except Exception:
                self.root_background = "transparent"
        else:
            self.root_background = "transparent"

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
        
        self.font_bold = ctk.CTkFont(weight="bold")
        self.font_title = ctk.CTkFont(size=20, weight="bold")
        self.font_large = ctk.CTkFont(size=16)
        self.font_large_italic = ctk.CTkFont(size=16, slant="italic")
        self.font_large_bold = ctk.CTkFont(size=16, weight="bold")
        self.font_subtitle = ctk.CTkFont(size=16, weight="bold")
        self.font_small = ctk.CTkFont(size=12)
        self.font_small_bold = ctk.CTkFont(size=12, weight="bold")
        self.font_13 = ctk.CTkFont(size=13)
        self.font_13_bold = ctk.CTkFont(size=13, weight="bold")
        self.font_medium_bold = ctk.CTkFont(size=14, weight="bold")
        self.font_navigation = ctk.CTkFont()

        self.navigation_buttons = [
            {
                "text": "Mod Updater",
                "icon": "mods.png",
                "command": self._show_mod_updater
            },
            {
                "text": "Kliko's mods",
                "icon": "marketplace.png",
                "command": self._show_marketplace
            },
            {
                "text": "Settings",
                "icon": "settings.png",
                "command": self._show_settings
            },
            {
                "text": "About",
                "icon": "about.png",
                "command": self._show_about
            }
        ]
        self._create_navigation()

        threading.Thread(
            name="MainWindow._load_marketplace_data()-thread",
            target=self._preload_marketplace_data,
            daemon=True
        ).start()

        self.content = ctk.CTkScrollableFrame(
            self.root,
            width=self.width-self.navigation_width,
            height=self.height,
            fg_color=self.root_background
        )
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid(column=1, row=0, sticky="nsew", padx=(4,0))

        self.root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        self.root.report_callback_exception = self._on_error
    
    def _on_error(self, *args) -> None:
        if len(args) > 1:
            error_message = str(args[1])
            error_type = type(args[1]).__name__

            if "object has no attribute 'focus_set'" in error_message:
                return

            else:
                print(args)
                print(f"{error_type}: {error_message}")

        error_handler.run(*args)

    def show(self) -> None:
        self._show_mod_updater()
        self.root.mainloop()

    # region Navigation
    def _create_navigation(self) -> None:
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
            if not os.path.isfile(light_icon_path):
                try:
                    restore_from_mei(light_icon_path)
                except (FileRestoreError, PermissionError, FileNotFoundError):
                    pass
            if not os.path.isfile(dark_icon_path):
                try:
                    restore_from_mei(dark_icon_path)
                except (FileRestoreError, PermissionError, FileNotFoundError):
                    pass
                
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
            ).grid(column=0, row=0, sticky="nsew", pady=(0,16))
    
            ctk.CTkLabel(
                header,
                text=ProjectData.NAME,
                anchor="center",
                justify="center",
                font=self.font_large
            ).grid(column=0, row=1, sticky="nsew")

            ctk.CTkLabel(
                header,
                text="Version "+ProjectData.VERSION,
                anchor="center",
                justify="center"
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
                    if not os.path.isfile(icon_path_light):
                        try:
                            restore_from_mei(icon_path_light)
                        except (FileRestoreError, PermissionError, FileNotFoundError):
                            pass
                    if not os.path.isfile(icon_path_dark):
                        try:
                            restore_from_mei(icon_path_dark)
                        except (FileRestoreError, PermissionError, FileNotFoundError):
                            pass
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
                    font=self.font_navigation,
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
    


    # region Mod updater
    def _show_mod_updater(self) -> None:
        def destroy() -> None:
            for widget in self.content.winfo_children():
                widget.destroy()

        def load_header() -> None:
            frame: ctk.CTkFrame = ctk.CTkFrame(
                self.content,
                fg_color="transparent"
            )
            frame.grid_columnconfigure(0, weight=1)
            frame.grid(column=0, row=0, sticky="nsew")

            ctk.CTkLabel(
                frame,
                text="Mod updater",
                font=self.font_title,
                anchor="w"
            ).grid(column=0, row=0, sticky="nsew")

            ctk.CTkLabel(
                frame,
                text="Update your mods",
                font=self.font_large,
                anchor="w"
            ).grid(column=0, row=1, sticky="nsew")
        
        def load_content() -> None:
            pass
            # TODO: Normal mode

            # TODO: Batch mode

            # TODO: Bloxstrap mode
            # bloxstrap_mode.run()

        self.active_section = "mod-updater"
        destroy()
        load_header()
        load_content()
    


    # region preload marketplace
    def _preload_marketplace_data(self) -> None:
        try:
            response: Response = request.get(GitHubApi.marketplace(), cache=True)
            data: list[dict] = response.json()

            for mod in data:
                if "has_thumbnail" in mod:
                    if mod["has_thumbnail"] == False:
                        continue
                load_image_from_url(GitHubApi.mod_thumbnail(mod["id"]), self.mod_thumbnail_size)
        
        except Exception as e:
            logger.warning(f"Failed to preload marketplace, reason: {type(e).__name__}: {e}")
    


    # region Marketplace
    def _show_marketplace(self) -> None:
        def destroy() -> None:
            for widget in self.content.winfo_children():
                widget.destroy()

        def load_header() -> None:
            frame: ctk.CTkFrame = ctk.CTkFrame(
                self.content,
                fg_color="transparent"
            )
            frame.grid_columnconfigure(0, weight=1)
            frame.grid(column=0, row=0, sticky="nsew")

            ctk.CTkLabel(
                frame,
                text="Kliko's mods",
                font=self.font_title,
                anchor="w"
            ).grid(column=0, row=0, sticky="nsew")

            ctk.CTkLabel(
                frame,
                text="Download mods with the press of a button",
                font=self.font_large,
                anchor="w"
            ).grid(column=0, row=1, sticky="nsew")
        
        def load_error(*args) -> None:
            ctk.CTkLabel(
                self.content,
                text="Marketplace failed to load!",
                font=self.font_title
            ).grid(column=0, row=1, sticky="nsew", pady=(64,0))

            error_box: ctk.CTkTextbox = ctk.CTkTextbox(
                self.content,
                wrap="word",
                fg_color="transparent"
            )
            error_box.insert("0.0", "".join(traceback.format_exception(*args)))
            error_box.configure(state="disabled")
            error_box.grid(column=0, row=2, sticky="nsew")
        
        def load_content() -> None:
            try:
                response: Response = request.get(GitHubApi.marketplace(), attempts=2, cache=True)
                data: list[dict] = response.json()

            except Exception as e:
                logger.error(f"Failed to load marketplace, reason: {type(e).__name__}: {e}")
                destroy()
                load_header()
                load_error(e)
            
            else:
                frame: ctk.CTkFrame = ctk.CTkFrame(
                    self.content,
                    fg_color="transparent"
                )
                frame.grid_columnconfigure(0, weight=1)
                frame.grid(column=0, row=1, sticky="nsew", padx=(0,10))

                for i, mod in enumerate(data):
                    try:
                        mod_name: str = mod["name"]
                        mod_id: str = mod["id"]
                        mod_author: str | None = mod.get("author" )
                        mod_description: str | None = mod.get("description")
                        mod_has_thumbnail: bool = mod.get("has_thumbnail", True)
                    
                    except KeyError:
                        continue

                    mod_frame: ctk.CTkFrame = ctk.CTkFrame(
                        frame
                    )
                    mod_frame.grid_columnconfigure(0, weight=1)
                    mod_frame.grid(column=0, row=i, sticky="ew", pady=5)

                    # Name, description, author
                    name_frame: ctk.CTkFrame = ctk.CTkFrame(
                        mod_frame,
                        fg_color="transparent"
                    )
                    name_frame.grid(column=0, row=0, sticky="nsew", padx=(16,0), pady=16)
                    
                    ctk.CTkLabel(
                        name_frame,
                        text=mod_name,
                        font=self.font_bold,
                        anchor="w",
                        justify="left"
                    ).grid(column=0, row=0, sticky="nsew")

                    if mod_description:
                        ctk.CTkLabel(
                            name_frame,
                            text=mod_description,
                            anchor="w",
                            justify="left"
                        ).grid(column=0, row=1, sticky="nsew")

                    if mod_author:
                        ctk.CTkLabel(
                            name_frame,
                            text=f"by {mod_author}",
                            font=self.font_13,
                            anchor="w",
                            justify="left"
                        ).grid(column=0, row=2, sticky="nsew")
                    
                    # Thumbnail
                    if mod_has_thumbnail:
                        ctk.CTkLabel(
                            mod_frame,
                            text="",
                            image=load_image_from_url(GitHubApi.mod_thumbnail(mod_id), self.mod_thumbnail_size)
                        ).grid(column=1, row=0, padx=32, pady=16)

                    # Download button
                    download_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "download.png")
                    if not os.path.isfile(download_icon):
                        try:
                            restore_from_mei(download_icon)
                        except (FileRestoreError, PermissionError, FileNotFoundError):
                            pass

                    ctk.CTkButton(
                        mod_frame,
                        text="",
                        image=load_image(
                            light=download_icon,
                            dark=download_icon,
                            size=(24,24)
                        ),
                        width=44,
                        height=44,
                        command=lambda mod_id=mod_id, mod_name=mod_name: self._mod_download(mod_id, mod_name)
                    ).grid(column=2, row=0, padx=32, pady=32)

        self.active_section = "marketplace"
        destroy()
        load_header()
        load_content()
    
    def _mod_download(self, mod_id: str, mod_name: str) -> None:
        if os.path.isdir(os.path.join(Directory.downloaded_mods(), mod_name)):
            if not messagebox.askokcancel(ProjectData.NAME, f"A mod with the same name already exists!\nDo you wish to overwrite it?"):
                return

        try:
            marketplace_mod_download(self, mod_id, mod_name)
            # messagebox.showinfo(ProjectData.NAME, "Mod downloaded successfully!")

        except Exception as e:
            logger.error(f"Failed to download mod \"{mod_id}\", reason: {type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to download mod: \"{mod_id}\"\n\n{type(e).__name__}: {e}")
    


    # region Settings
    def _show_settings(self) -> None:
        def destroy() -> None:
            for widget in self.content.winfo_children():
                widget.destroy()

        def load_header() -> None:
            frame: ctk.CTkFrame = ctk.CTkFrame(
                self.content,
                fg_color="transparent"
            )
            frame.grid_columnconfigure(0, weight=1)
            frame.grid(column=0, row=0, sticky="nsew")

            ctk.CTkLabel(
                frame,
                text="Settings",
                font=self.font_title,
                anchor="w"
            ).grid(column=0, row=0, sticky="nsew")

            ctk.CTkLabel(
                frame,
                text="Configure settings",
                font=self.font_large,
                anchor="w"
            ).grid(column=0, row=1, sticky="nsew")

            button_frame = ctk.CTkFrame(
                frame,
                fg_color="transparent"
            )
            button_frame.grid(column=0, row=2, sticky="nsew", pady=(16,16))

            restore_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "restore.png")
            if not os.path.isfile(restore_icon):
                try:
                    restore_from_mei(restore_icon)
                except (FileRestoreError, PermissionError, FileNotFoundError):
                    pass
            ctk.CTkButton(
                button_frame,
                text="Restore settings ",
                image=load_image(
                    light=restore_icon,
                    dark=restore_icon,
                    size=(24,24)
                ),
                width=1,
                anchor="w",
                compound=ctk.LEFT,
                command=self._restore_all_settings
            ).grid(column=0, row=0, sticky="nsw")
        
        def load_content() -> None:
            all_settings: dict[str, dict] = settings.get_all()

            if not all_settings:
                ctk.CTkLabel(
                    self.content,
                    text="No settings found!",
                    font=self.font_title
                ).grid(column=0, row=1, sticky="nsew", pady=(64,0))

            else:
                frame: ctk.CTkFrame = ctk.CTkFrame(
                    self.content,
                    fg_color="transparent"
                )
                frame.grid_columnconfigure(0, weight=1)
                frame.grid(column=0, row=1, sticky="nsew", padx=(0,10))

                for i, (key, data) in enumerate(all_settings.items()):
                    setting_frame: ctk.CTkFrame = ctk.CTkFrame(
                        frame
                    )
                    setting_frame.grid_columnconfigure(1, weight=1)
                    setting_frame.grid(column=0, row=i, sticky="ew", pady=5)

                    # Name and description
                    name_frame: ctk.CTkFrame = ctk.CTkFrame(
                        setting_frame,
                        fg_color="transparent"
                    )
                    name_frame.grid(column=0, row=0, sticky="w", padx=(16,0), pady=16)

                    ctk.CTkLabel(
                        name_frame,
                        text=str(data.get("name")),
                        anchor="w",
                        font=self.font_bold
                    ).grid(column=0, row=0, sticky="nsew")

                    if data.get("description"):
                        ctk.CTkLabel(
                            name_frame,
                            text=str(data.get("description")),
                            anchor="w",
                            font=self.font_13
                        ).grid(column=0, row=1, sticky="nsew")

                    # Value
                    # Toggle value
                    if data.get("type") == "bool":
                        var = ctk.BooleanVar(value=data.get("value"))
                        switch: ctk.CTkSwitch = ctk.CTkSwitch(
                            setting_frame,
                            width=48,
                            height=24,
                            text="",
                            variable=var,
                            onvalue=True,
                            offvalue=False,
                            command=lambda key=key, var=var: self._toggle_setting(key, var.get())
                        )
                        switch.grid(column=2, row=0, rowspan=2, sticky="ew", padx=32, pady=32)
                    
                    # Dropdown
                    elif data.get("type") == "choice":
                        options: list[dict] = data.get("options", [])
                        if not options:
                            continue
                        
                        value = next((item.get("name", "UNKNOWN") for item in options if item.get("value") == data.get("value")), "UNKNOWN")
                        var = ctk.StringVar(value=value)
                        dropdown: ctk.CTkComboBox = ctk.CTkComboBox(
                            setting_frame,
                            variable=var,
                            values=[option.get("name", "UNKNOWN") for option in options],
                            command=lambda _, key=key, var=var, options=options: self._set_setting_dropdown_value(key=key, value_key=var.get(), options=options)
                        )
                        dropdown.grid(column=2, row=0, rowspan=2, sticky="ew", padx=32, pady=32)

                    # Unknown setting type
                    else:
                        ctk.CTkLabel(
                            setting_frame,
                            text=f"Value: {data.get('value')}",
                            font=self.font_13
                        ).grid(column=2, row=0, rowspan=2, sticky="ew", padx=32, pady=32)
                    

        self.active_section = "settings"
        destroy()
        load_header()
        load_content()



    # region Configure settings
    def _toggle_setting(self, key: str, value: bool) -> None:
        settings.set_value(key, value)
    
    def _set_setting_dropdown_value(self, key: str, value_key: str, options: list[dict]) -> None:
        for option in options:
            if option.get("name") == value_key:
                value = option.get("value")
                break
        else:
            return
        settings.set_value(key, value)
    
    def _restore_all_settings(self) -> None:
        try:
            settings.restore_all()
            messagebox.showinfo(ProjectData.NAME, "Settings restored successfully!")
            self._show_settings()
        except Exception as e:
            logger.error(f"Failed to restore settings, reason: {type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to restore settings!\n\n{type(e).__name__}: {e}")



    # region About
    def _show_about(self) -> None:
        def destroy() -> None:
            for widget in self.content.winfo_children():
                widget.destroy()

        def load_header() -> None:
            frame: ctk.CTkFrame = ctk.CTkFrame(
                self.content,
                fg_color="transparent"
            )
            frame.grid_columnconfigure(1, weight=1)
            frame.grid(column=0, row=0, sticky="nsew", pady=(16,0))

            # Logo
            logo: str = os.path.join(Directory.root(), "resources", "menu", "about", "logo.png")
            if not os.path.isfile(logo):
                try:
                    restore_from_mei(logo)
                except (FileRestoreError, PermissionError, FileNotFoundError):
                    pass

            ctk.CTkLabel(
                frame,
                text="",
                image=load_image(
                    logo,
                    logo,
                    (64,64)
                )
            ).grid(column=0, row=0, sticky="nsew", padx=(0,12))
            
            # Info
            info_frame: ctk.CTkFrame = ctk.CTkFrame(
                frame,
                fg_color="transparent"
            )
            info_frame.grid_columnconfigure(1, weight=1)
            info_frame.grid(column=1, row=0, sticky="ew")

            ctk.CTkLabel(
                info_frame,
                text=ProjectData.NAME,
                font=self.font_title,
                anchor="w"
            ).grid(column=0, row=0, sticky="ew")

            ctk.CTkLabel(
                info_frame,
                text=f"v{ProjectData.VERSION}",
                font=self.font_bold,
                anchor="w"
            ).grid(column=1, row=0, sticky="ew", padx=(12,0))

            ctk.CTkLabel(
                info_frame,
                text=ProjectData.DESCRIPTION,
                font=self.font_large,
                anchor="w"
            ).grid(column=0, row=1, columnspan=2, sticky="ew")

            # Buttons
            button_frame = ctk.CTkFrame(
                frame,
                fg_color="transparent"
            )
            button_frame.grid(column=0, row=1, columnspan=2, sticky="nsew", pady=(12,24))

            github_icon: str = os.path.join(Directory.root(), "resources", "menu", "about", "github.png")
            if not os.path.isfile(github_icon):
                try:
                    restore_from_mei(github_icon)
                except (FileRestoreError, PermissionError, FileNotFoundError):
                    pass
            ctk.CTkButton(
                button_frame,
                text="Source Code ",
                image=load_image(
                    light=github_icon,
                    dark=github_icon,
                    size=(24,24)
                ),
                width=1,
                anchor="w",
                compound=ctk.LEFT,
                command=lambda: webbrowser.open_new_tab(Hyperlink.GITHUB)
            ).grid(column=0, row=0, sticky="nsw")

            discord_icon: str = os.path.join(Directory.root(), "resources", "menu", "about", "discord.png")
            if not os.path.isfile(discord_icon):
                try:
                    restore_from_mei(discord_icon)
                except (FileRestoreError, PermissionError, FileNotFoundError):
                    pass
            ctk.CTkButton(
                button_frame,
                text="Discord ",
                image=load_image(
                    light=discord_icon,
                    dark=discord_icon,
                    size=(24,24)
                ),
                width=1,
                anchor="w",
                compound=ctk.LEFT,
                command=lambda: webbrowser.open_new_tab(Hyperlink.DISCORD)
            ).grid(column=1, row=0, sticky="nsw", padx=(8,0))
        
        def load_content() -> None:
            # Licenses
            licenses_per_row: int = 3
            license_gap: int = 8

            license_frame: ctk.CTkFrame = ctk.CTkFrame(
                self.content,
                fg_color="transparent"
            )
            license_frame.grid(column=0, row=1, sticky="nsew")
            for i in range(licenses_per_row):
                license_frame.grid_columnconfigure(i, weight=0)

            ctk.CTkLabel(
                license_frame,
                text="Licenses",
                font=self.font_large_bold,
                anchor="w",
                justify="left"
            ).grid(column=0, row=0, sticky="nsew")

            for i, license in enumerate(LICENSES):
                column = int(i % licenses_per_row)
                row = int((i // licenses_per_row)) + 1
                padx = 0 if column == 0 else (license_gap, 0)
                pady = 0 if row == 0 else (license_gap, 0)
                license_box: ctk.CTkFrame = ctk.CTkFrame(
                    license_frame,
                    width=250,
                    height=120
                )
                license_box.grid_propagate(False)
                license_box.grid(column=column, row=row, padx=padx, pady=pady, sticky="nsew")
                
                box_content: ctk.CTkFrame = ctk.CTkFrame(
                    license_box,
                    fg_color="transparent"
                )
                box_content.grid(column=0, row=0, padx=16, pady=16)

                ctk.CTkLabel(
                    box_content,
                    text=license["name"],
                    font=self.font_bold,
                    anchor="w",
                    justify="left"
                ).grid(column=0, row=0, sticky="nsew")

                ctk.CTkLabel(
                    box_content,
                    text=f"by {license['author']}",
                    anchor="w",
                    justify="left"
                ).grid(column=0, row=1, sticky="nsew")

                ctk.CTkLabel(
                    box_content,
                    text=license["type"],
                    font=self.font_13,
                    anchor="w",
                    justify="left"
                ).grid(column=0, row=2, sticky="nsew")

                
                if license.get("url"):
                    license_box.configure(cursor="hand2")
                    license_box.bind("<Button-1>", lambda _, url=license["url"]: webbrowser.open_new_tab(url))
                    for widget in box_content.winfo_children():
                        widget.bind("<Button-1>", lambda _, url=license["url"]: webbrowser.open_new_tab(url))

        self.active_section = "about"
        destroy()
        load_header()
        load_content()