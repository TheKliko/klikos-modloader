import os
import sys
import shutil
import json
import re
from datetime import datetime
from typing import Callable, Literal
from tempfile import TemporaryDirectory

from modules.logger import logger
from modules.info import ProjectData
from modules.filesystem import Directory
from modules import filesystem
from modules.interface.images import load_image
from modules.functions.restore_from_mei import restore_from_mei, FileRestoreError
from modules.functions.config import mods, fastflags
from modules.functions.get_latest_version import get_latest_version
from modules import request
from modules.request import RobloxApi, GitHubApi, RequestError, Response

from tkinter import filedialog, messagebox
import customtkinter as ctk
from fontTools.ttLib import TTFont
import pyperclip


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

    title: str = "Modloader Menu"
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
        self.font_subtitle = ctk.CTkFont(size=16, weight="bold")
        self.font_small = ctk.CTkFont(size=12)
        self.font_small_bold = ctk.CTkFont(size=12, weight="bold")
        self.font_13 = ctk.CTkFont(size=13)
        self.font_13_bold = ctk.CTkFont(size=13, weight="bold")
        self.font_medium_bold = ctk.CTkFont(size=14, weight="bold")
        self.font_navigation = ctk.CTkFont()

        self.navigation_buttons = [
            {
                "text": "Mods",
                "icon": "mods.png",
                "command": self._show_mods
            },
            {
                "text": "Community Mods",
                "icon": "marketplace.png",
                "command": self._show_marketplace
            },
            {
                "text": "FastFlags",
                "icon": "fastflags.png",
                "command": self._show_fastflags
            },
            {
                "text": "Integrations",
                "icon": "integrations.png",
                "command": self._show_integrations
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

        self.content = ctk.CTkScrollableFrame(
            self.root,
            width=self.width-self.navigation_width,
            height=self.height,
            fg_color=self.root_background
        )
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid(column=1, row=0, sticky="nsew", padx=(4,0))

        self.root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

    def show(self) -> None:
        self._show_mods()
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

    # region Mods
    def _show_mods(self) -> None:
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
                text="Mods",
                font=self.font_title,
                anchor="w"
            ).grid(column=0, row=0, sticky="nsew")

            ctk.CTkLabel(
                frame,
                text="Manage your mods",
                font=self.font_large,
                anchor="w"
            ).grid(column=0, row=1, sticky="nsew")

            button_frame = ctk.CTkFrame(
                frame,
                fg_color="transparent"
            )
            button_frame.grid(column=0, row=2, sticky="nsew", pady=(16,16))

            package_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "package.png")
            if not os.path.isfile(package_icon):
                try:
                    restore_from_mei(package_icon)
                except (FileRestoreError, PermissionError, FileNotFoundError):
                    pass
            ctk.CTkButton(
                button_frame,
                text="Add mods",
                image=load_image(
                    light=package_icon,
                    dark=package_icon,
                    size=(24,24)
                ),
                width=1,
                anchor="w",
                compound=ctk.LEFT,
                command=self._import_mod
            ).grid(column=0, row=0, sticky="nsw")

            folder_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "folder.png")
            if not os.path.isfile(folder_icon):
                try:
                    restore_from_mei(folder_icon)
                except (FileRestoreError, PermissionError, FileNotFoundError):
                    pass
            ctk.CTkButton(
                button_frame,
                text="Open mods folder",
                image=load_image(
                    light=folder_icon,
                    dark=folder_icon,
                    size=(24,24)
                ),
                width=1,
                anchor="w",
                compound=ctk.LEFT,
                command=lambda: filesystem.open(Directory.mods())
            ).grid(column=1, row=0, sticky="nsw", padx=(8,0))

            font_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "font.png")
            if not os.path.isfile(font_icon):
                try:
                    restore_from_mei(font_icon)
                except (FileRestoreError, PermissionError, FileNotFoundError):
                    pass
            ctk.CTkButton(
                button_frame,
                text="Add font",
                image=load_image(
                    light=font_icon,
                    dark=font_icon,
                    size=(24,24)
                ),
                width=1,
                anchor="w",
                compound=ctk.LEFT,
                command=self._create_font_mod
            ).grid(column=2, row=0, sticky="nsw", padx=(8,0))

        def load_content() -> None:
            mods_directory: str = Directory.mods()
            installed_mods: list = [mod for mod in os.listdir(mods_directory) if os.path.isdir(os.path.join(mods_directory, mod))]
            mod_data: dict = mods.get_all()
            configured_mods: list[str] = [mod["name"] for mod in mod_data]

            if not installed_mods:
                ctk.CTkLabel(
                    self.content,
                    text="No mods found!",
                    font=self.font_title
                ).grid(column=0, row=1, sticky="nsew", pady=(64,0))

            else:
                frame: ctk.CTkFrame = ctk.CTkFrame(
                    self.content,
                    fg_color="transparent"
                )
                frame.grid_columnconfigure(0, weight=1)
                frame.grid(column=0, row=1, sticky="nsew", padx=(0,10))
                for i, mod in enumerate(installed_mods):
                    is_configured: bool = mod in configured_mods
                    if is_configured:
                        data: dict = mods.get(mod)
                        priority: int = data["priority"]
                        enabled: bool = data["enabled"]
                    else:
                        priority = 0
                        enabled = False
                    mod_info = {"name": mod}

                    mod_frame: ctk.CTkFrame = ctk.CTkFrame(
                        frame
                    )
                    mod_frame.grid_columnconfigure(1, weight=1)
                    mod_frame.grid(column=0, row=i, sticky="ew", pady=10)

                    # Delete button
                    delete_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "remove.png")
                    if not os.path.isfile(delete_icon):
                        try:
                            restore_from_mei(delete_icon)
                        except (FileRestoreError, PermissionError, FileNotFoundError):
                            pass
                    ctk.CTkButton(
                        mod_frame,
                        text="",
                        image=load_image(
                            light=delete_icon,
                            dark=delete_icon,
                            size=(24,24)
                        ),
                        width=44,
                        height=44,
                        command=lambda mod_info=mod_info: self._delete_mod(
                            name=mod_info["name"]
                        )
                    ).grid(column=0, row=0, rowspan=2, padx=16, pady=16)

                    # Name label
                    name_frame: ctk.CTkFrame = ctk.CTkFrame(
                        mod_frame,
                        fg_color="transparent"
                    )
                    name_frame.grid(column=1, row=0, sticky="nsew")
                    name_entry = ctk.CTkEntry(
                        name_frame,
                        width=250,
                        height=40,
                        validate="key",
                        validatecommand=(self.root.register(lambda value: not re.search(r'[\\/:*?"<>|]', value)), '%P')
                    )
                    name_entry.insert("end", str(mod))
                    name_entry.bind("<Return>", lambda _: self.root.focus())
                    name_entry.bind("<Control-s>", lambda _: self.root.focus())
                    name_entry.bind("<FocusOut>", lambda event, mod_info=mod_info: self._rename_mod(event, mod_info))
                    name_entry.grid(column=0, row=0, sticky="nsew", pady=24)

                    # Load order frame
                    load_order_frame: ctk.CTkFrame = ctk.CTkFrame(
                        mod_frame,
                        fg_color="transparent"
                    )
                    load_order_frame.grid(column=2, row=0, rowspan=2, padx=16, pady=16)

                    ctk.CTkLabel(
                        load_order_frame,
                        text="Load order:",
                        anchor="w",
                        justify="left"
                    ).grid(column=0, row=0, sticky="nsew")

                    entry = ctk.CTkEntry(
                        load_order_frame,
                        width=40,
                        height=40,
                        validate="key",
                        validatecommand=(self.root.register(lambda value: value.isdigit() or value == ""), '%P')
                    )
                    entry.insert("end", str(priority))
                    entry.bind("<Return>", lambda _: self.root.focus())
                    entry.bind("<Control-s>", lambda _: self.root.focus())
                    entry.bind("<FocusOut>", lambda event, mod_info=mod_info: self._set_mod_priority(event, mod_info["name"]))
                    entry.grid(column=1, row=0, sticky="nsew", padx=16)

                    # Toggle active state
                    var = ctk.BooleanVar(value=enabled)
                    switch: ctk.CTkSwitch = ctk.CTkSwitch(
                        mod_frame,
                        width=48,
                        height=24,
                        text="",
                        variable=var,
                        onvalue=True,
                        offvalue=False,
                        command=lambda mod_info=mod_info, status_var=var: self._set_mod_status(mod_info["name"], status_var.get())
                    )
                    switch.grid(column=3, row=0, rowspan=2, sticky="ew", padx=32, pady=32)


        self.active_section = "mods"
        destroy()
        load_header()
        load_content()

    # region Importing mods
    def _import_mod(self) -> None:
        user_profile: str | None = os.getenv("HOME") or os.getenv("USERPROFILE")
        initial_dir: str = os.path.join(user_profile, "Downloads") if user_profile is not None else os.path.abspath(os.sep)
        files_to_import = filedialog.askopenfilenames(
            filetypes=[
                ("Archive files", "*.zip;*.7z"),
                ("ZIP archives", "*.zip"),
                ("7z archives", "*.7z")
            ],
            initialdir=initial_dir,
            title="Import mods"
        )

        if not files_to_import:
            return
        
        for file in files_to_import:
            mod_name: str = os.path.basename(file).removesuffix(".zip").removesuffix(".7z")
            target: str = os.path.join(Directory.mods(), mod_name)
            
            if os.path.isdir(target):
                if not messagebox.askokcancel(ProjectData.NAME, f"A mod named \"{mod_name}\" already exists!\nDo you still wish to import it?"):
                    continue
                shutil.rmtree(target, ignore_errors=True)
            
            try:
                filesystem.extract(file, target)
            except Exception as e:
                logger.error(f"Failed to import mod: {mod_name}, {type(e).__name__}: {e}")
                messagebox.showerror(ProjectData.NAME, f"Failed to import mod:\n\"{mod_name}\"\n\n{type(e).__name__}: {e}")

        self._show_mods()

    # region Font mods
    # TODO: Load fonts from URL
    def _create_font_mod(self) -> None:
        class Window(ctk.CTkToplevel):

            result: tuple[str, str] | None = None
            URL_MODE: str = "url"
            FILE_MODE: str = "file"

            entry_width: int = 360
            button_size: tuple[int, int] = (44, 44)
            icon_size: tuple[int, int] = (24, 24)

            def __init__(self, root, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self.root = root

                if self.root.icon is not None:
                    self.iconbitmap(self.root.icon)
                    self.after(200, lambda: self.iconbitmap(self.root.icon))
                self.title("Font selector")

                self.protocol("WM_DELETE_WINDOW", self._on_close)
                self.bind("<Escape>", lambda _: self._on_close())

                file_select_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "file_select.png")
                run_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "run.png")
                
                if not os.path.isfile(file_select_icon):
                    try:
                        restore_from_mei(file_select_icon)
                    except (FileRestoreError, PermissionError, FileNotFoundError):
                        pass
                if not os.path.isfile(run_icon):
                    try:
                        restore_from_mei(run_icon)
                    except (FileRestoreError, PermissionError, FileNotFoundError):
                        pass

                # Font from file
                self.file_frame = ctk.CTkFrame(
                    self,
                    fg_color="transparent"
                )
                self.file_frame.grid(column=0, row=0, sticky="nsew", padx=32, pady=(32,32))
                self.file_frame.grid_columnconfigure(0, weight=1)
                self.filepath = ctk.StringVar(value="")

                # ctk.CTkLabel(
                #     self.file_frame,
                #     text="Load from file:",
                #     font=self.root.font_bold
                # ).grid(column=0, row=0, sticky="ns", padx=(0,8))

                self.file_entry: ctk.CTkEntry = ctk.CTkEntry(
                    self.file_frame,
                    width=self.entry_width-self.button_size[0]-8,
                    height=self.button_size[1],
                    placeholder_text="Choose a file"
                )
                self.file_entry.configure(state="disabled")
                self.file_entry.grid(column=1, row=0, sticky="ns")

                ctk.CTkButton(
                    self.file_frame,
                    text="",
                    width=self.button_size[0],
                    height=self.button_size[1],
                    image=load_image(
                        light=file_select_icon,
                        dark=file_select_icon,
                        size=self.icon_size
                    ),
                    command=self._choose_file
                ).grid(column=2, row=0, sticky="ns", padx=(8,0))

                ctk.CTkButton(
                    self.file_frame,
                    text="",
                    width=self.button_size[0],
                    height=self.button_size[1],
                    image=load_image(
                        light=run_icon,
                        dark=run_icon,
                        size=self.icon_size
                    ),
                    command=lambda: self._on_run(mode=self.FILE_MODE, data=self.filepath)
                ).grid(column=3, row=0, sticky="ns", padx=(16,0))

                # Font from URL
                # self.url_frame = ctk.CTkFrame(
                #     self,
                #     fg_color="transparent"
                # )
                # self.url_frame.grid(column=0, row=1, sticky="nsew", padx=32, pady=(16,32))
                # self.url_frame.grid_columnconfigure(0, weight=1)
                # self.url = ctk.StringVar(value="")

                # ctk.CTkLabel(
                #     self.url_frame,
                #     text="Load from URL:",
                #     font=self.root.font_bold
                # ).grid(column=0, row=0, sticky="ns", padx=(0,8))

                # ctk.CTkEntry(
                #     self.url_frame,
                #     width=self.entry_width,
                #     height=self.button_size[1],
                #     placeholder_text="URL",
                #     textvariable=self.url
                # ).grid(column=1, row=0, sticky="ns")

                # ctk.CTkButton(
                #     self.url_frame,
                #     text="",
                #     width=self.button_size[0],
                #     height=self.button_size[1],
                #     image=load_image(
                #         light=run_icon,
                #         dark=run_icon,
                #         size=self.icon_size
                #     ),
                #     command=lambda: self._on_run(mode=self.URL_MODE, data=self.url)
                # ).grid(column=2, row=0, sticky="ns", padx=(16,0))

                self.update_idletasks()
                width = self.winfo_reqwidth()
                height = self.winfo_reqheight()
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()
                x = (screen_width // 2) - (width // 2)
                y = (screen_height // 2) - (height // 2)
                self.geometry(f"{width}x{height}+{x}+{y}")
                self.resizable(False, False)

                
            def show(self) -> tuple[str, str] | None:
                self.focus()
                self.grab_set()
                self.wait_window()
                return self.result
            
            def _choose_file(self) -> None:
                user_profile: str | None = os.getenv("HOME") or os.getenv("USERPROFILE")
                initial_dir: str = os.path.join(user_profile, "Downloads") if user_profile is not None else os.path.abspath(os.sep)
                font_file = filedialog.askopenfilename(
                    filetypes=[
                        ("Font files", "*.ttf;*.otf"),
                        ("TrueType Fonts", "*.ttf"),
                        ("OpenType Fonts", "*.otf")
                    ],
                    initialdir=initial_dir,
                    title="Choose a font"
                )
                if not font_file:
                    return
                self.filepath = font_file
                self.file_entry.configure(state="normal")
                self.file_entry.delete(0, "end")
                self.file_entry.insert(0, os.path.basename(self.filepath))
                self.file_entry.configure(state="disabled")

            
            def _on_close(self) -> None:
                self.grab_release()
                self.destroy()
            
            def _on_run(self, mode: str, data: str) -> None:
                self.result = (mode, data)
                self._on_close()

        window = Window(self)
        result = window.show()
        if not result:
            return
        
        mode: str = result[0]

        if mode == window.FILE_MODE:
            filepath: str = result[1]

            if not os.path.isfile(filepath):
                messagebox.showerror(ProjectData.NAME, "Failed to create font mod!\n\nFile does not exist.")
                return

            mod_name: str = f"Font ({os.path.basename(filepath).split('.')[0]})"
            target: str = os.path.join(Directory.mods(), mod_name)

            rbxasset_new: str = "rbxasset://fonts/CustomFont.ttf"
            try:
                with TemporaryDirectory() as temp_directory:
                    source: str = os.path.join(temp_directory, mod_name)
                    font_basepath: str = os.path.join(source, "content", "fonts")
                    font_path: str = os.path.join(font_basepath, "CustomFont.ttf")
                    font_families_path: str = os.path.join(font_basepath, "families")
                    os.makedirs(font_families_path)

                    if filepath.endswith(".ttf"):
                        shutil.copyfile(filepath, font_path)
                    else:
                        TTFont(filepath).save(font_path)
                    
                    latest_version: str = get_latest_version(binary_type="WindowsPlayer")
                    filesystem.download(RobloxApi.download(latest_version, "content-fonts.zip"), os.path.join(temp_directory, "roblox_fonts.zip"))
                    filesystem.extract(os.path.join(temp_directory, "roblox_fonts.zip"), os.path.join(temp_directory, "roblox_fonts"))

                    roblox_font_families_path: str = os.path.join(temp_directory, "roblox_fonts", "families")
                    shutil.copytree(roblox_font_families_path, font_families_path, dirs_exist_ok=True)
                    
                    for json_file in [os.path.join(font_families_path, item) for item in os.listdir(font_families_path) if os.path.join(font_families_path, item) and item.endswith(".json")]:
                        with open(json_file, "r") as read_file:
                            data: dict = json.load(read_file)
                        font_faces: list = data.get("faces", [])
                        if not font_faces:
                            continue
                        for i in range(len(font_faces)):
                            font_faces[i]["assetId"] = rbxasset_new
                        data["faces"] = font_faces
                        with open(json_file, "w") as write_file:
                            json.dump(data, write_file, indent=4)

                    if os.path.isdir(target):
                        shutil.rmtree(target, ignore_errors=True)
                    shutil.copytree(source, target, dirs_exist_ok=True)

            except Exception as e:
                logger.error(f"Failed to create font mod, {type(e).__name__}: {e}")
                messagebox.showerror(ProjectData.NAME, f"Failed to create font mod!\n\n{type(e).__name__}: {e}")

        else:
            raise NotImplementedError(f"Failed to generate font mod!\n Unknown mode: {mode}")
        # elif mode == window.URL_MODE:
        #     url: str = result[1]
        #     messagebox.showinfo("test", "URLMODE")

        self._show_mods()

    # region Configure mod
    def _set_mod_status(self, name: str, status: bool) -> None:
        try:
            mods.set_status(name, status)
        except Exception as e:
            logger.error(f"Failed to update mod status, {type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to update mod status!\n\n{type(e).__name__}: {e}")

    def _set_mod_priority(self, event, name: str) -> None:
        try:
            priority: int = int(event.widget.get())
        except Exception as e:
            logger.error(f"Failed to update mod priority!\n\n{type(e).__name__}: {e}")
            event.widget.delete(0, "end")
            event.widget.insert(0, str(mods.get(name).get("priority", mods.FORMAT["priority"])))
            return

        try:
            mods.set_priority(name, priority)
        except Exception as e:
            logger.error(f"Failed to update mod priority! {type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to update mod priority!\n\n{type(e).__name__}: {e}")
    
    def _rename_mod(self, event, mod_info) -> None:
        name: str = mod_info["name"]
        new_name: str = str(event.widget.get())
        if name == new_name:
            return
        
        if not new_name:
            event.widget.delete(0, "end")
            event.widget.insert(0, name)
            return

        mods_directory: str = Directory.mods()
        try:
            os.rename(os.path.join(mods_directory, name), os.path.join(mods_directory, new_name))
        except FileExistsError:
            messagebox.showerror(ProjectData.NAME, "Failed to rename mod!\nAnother mod with the same name already exists!")
            return
        except Exception as e:
            logger.error(f"Failed to rename mod: \"{name}\", {type(e).__name__}: {e}")
            messagebox.showwarning(ProjectData.NAME, f"Failed to rename mod:\n\"{name}\"\n\n{type(e).__name__}: {e}")
            return

        mods.set_name(name, new_name)
        mod_info["name"] = new_name
        # self._show_mods()
    
    def _delete_mod(self, name: str) -> None:
        if not messagebox.askokcancel(ProjectData.NAME, f"Are you sure you want to delete this mod:\n\"{name}\"\n\nThis action cannot be undone!"):
            return

        try:
            filesystem.remove(os.path.join(Directory.mods(), name))
        except Exception as e:
            logger.error(f"Failed to delete mod \"{name}\"\n{type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to delete mod:\n\"{name}\"\n\n{type(e).__name__}: {e}")
            return
        
        try:
            mods.remove(name)
        except Exception:
            pass
        self._show_mods()

    # region FastFlags
    def _show_fastflags(self) -> None:
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
                text="FastFlags",
                font=self.font_title,
                anchor="w"
            ).grid(column=0, row=0, sticky="nsew")

            ctk.CTkLabel(
                frame,
                text="Manage your FastFlags",
                font=self.font_large,
                anchor="w"
            ).grid(column=0, row=1, sticky="nsew")

            button_frame = ctk.CTkFrame(
                frame,
                fg_color="transparent"
            )
            button_frame.grid(column=0, row=2, sticky="nsew", pady=(16,16))

            plus_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "create.png")
            if not os.path.isfile(plus_icon):
                try:
                    restore_from_mei(plus_icon)
                except (FileRestoreError, PermissionError, FileNotFoundError):
                    pass
            ctk.CTkButton(
                button_frame,
                text="New profile",
                image=load_image(
                    light=plus_icon,
                    dark=plus_icon,
                    size=(24,24)
                ),
                width=1,
                anchor="w",
                compound=ctk.LEFT,
                command=self._create_fastflag_profile
            ).grid(column=0, row=0, sticky="nsw")

            download_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "cloud-download.png")
            if not os.path.isfile(download_icon):
                try:
                    restore_from_mei(download_icon)
                except (FileRestoreError, PermissionError, FileNotFoundError):
                    pass
            ctk.CTkButton(
                button_frame,
                text="FastFlag presets",
                image=load_image(
                    light=download_icon,
                    dark=download_icon,
                    size=(24,24)
                ),
                width=1,
                anchor="w",
                compound=ctk.LEFT,
                command=self._import_fastflag_preset
            ).grid(column=1, row=0, sticky="nsw", padx=(8,0))
        
        def load_content() -> None:
            profiles: list[dict] = fastflags.get_all()

            if not profiles:
                ctk.CTkLabel(
                    self.content,
                    text="No profiles found!",
                    font=self.font_title
                ).grid(column=0, row=1, sticky="nsew", pady=(64,0))

            else:
                frame: ctk.CTkFrame = ctk.CTkFrame(
                    self.content,
                    fg_color="transparent"
                )
                frame.grid_columnconfigure(0, weight=1)
                frame.grid(column=0, row=1, sticky="nsew", padx=(0,10))

                for i, profile in enumerate(profiles):
                    name: str | None = profile.get("name")
                    description: str | None = profile.get("description")
                    enabled: bool = profile.get("enabled", False)
                    data: dict = profile.get("data", {})

                    profile_info = {
                        "name": name,
                        "description": description,
                        "enabled": enabled,
                        "data": data
                    }

                    if not name:
                        continue

                    profile_frame: ctk.CTkFrame = ctk.CTkFrame(
                        frame
                    )
                    profile_frame.grid_columnconfigure(1, weight=1)
                    profile_frame.grid(column=0, row=i, sticky="ew", pady=10)

                    # Delete button
                    delete_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "remove.png")
                    if not os.path.isfile(delete_icon):
                        try:
                            restore_from_mei(delete_icon)
                        except (FileRestoreError, PermissionError, FileNotFoundError):
                            pass
                    ctk.CTkButton(
                        profile_frame,
                        text="",
                        image=load_image(
                            light=delete_icon,
                            dark=delete_icon,
                            size=(24,24)
                        ),
                        width=44,
                        height=44,
                        command=lambda profile_info=profile_info: self._delete_fastflag_profile(
                            name=profile_info["name"]
                        )
                    ).grid(column=0, row=0, rowspan=2, padx=16, pady=16)

                    # Name label
                    name_frame: ctk.CTkFrame = ctk.CTkFrame(
                        profile_frame,
                        fg_color="transparent"
                    )
                    name_frame.grid(column=1, row=0, sticky="nsew")
                    name_entry = ctk.CTkEntry(
                        name_frame,
                        width=250,
                        height=40
                    )
                    name_entry.insert("end", name)
                    name_entry.bind("<Return>", lambda _: self.root.focus())
                    name_entry.bind("<Control-s>", lambda _: self.root.focus())
                    name_entry.bind("<FocusOut>", lambda event, profile_info=profile_info: self._rename_fastflag_profile(event, profile_info))
                    name_entry.grid(column=0, row=0, sticky="nsew", pady=24)

                    # Configure profile
                    configure_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "configure.png")
                    if not os.path.isfile(configure_icon):
                        try:
                            restore_from_mei(configure_icon)
                        except (FileRestoreError, PermissionError, FileNotFoundError):
                            pass

                    ctk.CTkButton(
                        profile_frame,
                        text="Configure",
                        image=load_image(
                            configure_icon,
                            configure_icon,
                            (24,24)
                        ),
                        height=44,
                        command=lambda profile_info=profile_info: self._configure_fastflag_profile(profile_info)
                    ).grid(column=2, row=0, rowspan=2, padx=(16,32), pady=16)

                    # Toggle active state
                    var = ctk.BooleanVar(value=enabled)
                    switch: ctk.CTkSwitch = ctk.CTkSwitch(
                        profile_frame,
                        width=48,
                        height=24,
                        text="",
                        variable=var,
                        onvalue=True,
                        offvalue=False,
                        command=lambda profile_info=profile_info, status_var=var: self._set_fastflag_profile_status(profile_info["name"], status_var.get())
                    )
                    switch.grid(column=3, row=0, rowspan=2, sticky="ew", padx=32, pady=32)

        self.active_section = "fastflags"
        destroy()
        load_header()
        load_content()
    
    #region FastFlags 2
    def _configure_fastflag_profile(self, profile_info: dict) -> None:
        class Window(ctk.CTkToplevel):
            
            def __init__(self, root, profile_info: dict, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self.root = root
                self.profile_info = profile_info

                if self.root.icon is not None:
                    self.iconbitmap(self.root.icon)
                    self.after(200, lambda: self.iconbitmap(self.root.icon))
                self.title("FastFlag configuration")

                self.protocol("WM_DELETE_WINDOW", self._on_close)
                self.bind("<Escape>", lambda _: self._on_close())

                self.grid_columnconfigure(0, weight=1)
                self.grid_rowconfigure(5, weight=1)


                # Name
                ctk.CTkLabel(
                    self,
                    text="Name:",
                    font=self.root.font_13_bold,
                    anchor="w"
                ).grid(column=0, row=0, sticky="nsew", padx=32, pady=(32,0))
                self.name_entry = ctk.CTkEntry(
                    self,
                    width=250,
                    height=40
                )
                self.name_entry.insert("end", self.profile_info["name"])
                self.name_entry.bind("<Return>", lambda _: self.focus())
                self.name_entry.bind("<Control-s>", lambda _: self.focus())
                self.name_entry.bind("<FocusOut>", lambda event, profile_info=self.profile_info: self.root._rename_fastflag_profile(event, profile_info))
                self.name_entry.grid(column=0, row=1, sticky="nsew", padx=32)

                # Description
                ctk.CTkLabel(
                    self,
                    text="Description:",
                    font=self.root.font_13_bold,
                    anchor="w"
                ).grid(column=0, row=2, sticky="nsew", padx=32, pady=(16,0))
                description_textbox = ctk.CTkTextbox(
                    self,
                    width=250,
                    height=56,
                    wrap="word"
                )
                description_textbox.insert("end", self.profile_info["description"] or "")
                # description_textbox.bind("<Return>", lambda _: self.focus())
                description_textbox.bind("<Control-s>", lambda _: self.focus())
                description_textbox.bind("<FocusOut>", lambda event, profile_info=self.profile_info: self.root._set_fastflag_profile_description(event, profile_info))
                description_textbox.grid(column=0, row=3, sticky="nsew", padx=32)

                # Data
                ctk.CTkLabel(
                    self,
                    text="Data:",
                    font=self.root.font_13_bold,
                    anchor="w"
                ).grid(column=0, row=4, sticky="nsew", padx=32, pady=(16,0))
                self.data_textbox = ctk.CTkTextbox(
                    self,
                    width=250,
                    height=400,
                    wrap="word",
                    text_color="#9cdcfe"
                )
                self.data_textbox.insert("end", json.dumps(self.profile_info["data"], indent=4))
                # self.data_textbox.bind("<Return>", lambda _: self.focus())
                self.data_textbox.bind("<Control-s>", lambda _: self.focus())
                self.data_textbox.bind("<FocusOut>", lambda event, profile_info=self.profile_info: self.root._set_fastflag_profile_data(event, profile_info))
                self.data_textbox.grid(column=0, row=5, sticky="nsew", padx=32, pady=(0,16))

                # Buttons
                export_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "export.png")
                import_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "import.png")
                copy_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "copy.png")
                rename_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "rename.png")
                delete_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "remove.png")

                if not os.path.isfile(export_icon):
                    try:
                        restore_from_mei(export_icon)
                    except (FileRestoreError, PermissionError, FileNotFoundError):
                        pass
                if not os.path.isfile(import_icon):
                    try:
                        restore_from_mei(import_icon)
                    except (FileRestoreError, PermissionError, FileNotFoundError):
                        pass
                if not os.path.isfile(copy_icon):
                    try:
                        restore_from_mei(copy_icon)
                    except (FileRestoreError, PermissionError, FileNotFoundError):
                        pass
                if not os.path.isfile(rename_icon):
                    try:
                        restore_from_mei(rename_icon)
                    except (FileRestoreError, PermissionError, FileNotFoundError):
                        pass
                if not os.path.isfile(delete_icon):
                    try:
                        restore_from_mei(delete_icon)
                    except (FileRestoreError, PermissionError, FileNotFoundError):
                        pass

                icon_size: tuple[int,int] = (24,24)

                buttons_per_row: int = 5
                buttons: list[dict] = [
                    {
                        "text": "Import data",
                        "image": import_icon,
                        "command": self._on_import
                    },
                    {
                        "text": "Export data",
                        "image": export_icon,
                        "command": self._on_export
                    },
                    {
                        "text": "Copy to clipboard",
                        "image": copy_icon,
                        "command": self._on_copy
                    }
                ]

                button_frame = ctk.CTkFrame(
                    self,
                    fg_color="transparent"
                )
                button_frame.grid(column=0, row=6, padx=32, pady=(0,32), sticky="nsew")

                for i, data in enumerate(buttons):
                    column: int = i % buttons_per_row
                    row: int = i // buttons_per_row

                    icon = data.get("image", "")

                    ctk.CTkButton(
                        button_frame,
                        text=data.get("text", ""),
                        image=load_image(
                            icon,
                            icon,
                            icon_size
                        ),
                        command=data.get("command"),
                        compound=ctk.LEFT,
                        height=44
                    ).grid(column=column, row=row, padx=(0,4), pady=(4,0))


                self.update_idletasks()
                # width = self.winfo_reqwidth()
                # height = self.winfo_reqheight()
                width = 600
                height = 450
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()
                x = (screen_width // 2) - (width // 2)
                y = (screen_height // 2) - (height // 2)
                self.geometry(f"{width}x{height}+{x}+{y}")
                self.minsize(width, height)
                # self.resizable(False, False)


            def show(self) -> None:
                self.focus()
                self.grab_set()
                self.wait_window()


            def _on_close(self) -> None:
                self.focus()
                self.grab_release()
                self.destroy()
            

            def _on_import(self) -> None:
                try:
                    data_string: str = self.data_textbox.get("0.0", "end")
                    try:
                        data: dict = json.loads(data_string)
                    except Exception as e:
                        logger.error(f"Unable to import data, reason: {type(e).__name__}: {e}")
                        messagebox.showerror(ProjectData.NAME, f"Unable to import data!\n\n{type(e).__name__}: {e}")
                        return

                    user_profile: str | None = os.getenv("HOME") or os.getenv("USERPROFILE")
                    initial_dir: str = os.path.join(user_profile, "Downloads") if user_profile is not None else os.path.abspath(os.sep)
                    files_to_import = filedialog.askopenfilenames(
                        filetypes=[
                            ("JSON files", "*.json"),
                        ],
                        initialdir=initial_dir,
                        title="Import data"
                    )

                    if not files_to_import:
                        return
                    
                    for filepath in files_to_import:
                        try:
                            with open(filepath, "r") as file:
                                import_data: dict = json.load(file)
                            data.update(import_data)
                            self.data_textbox.delete("0.0", "end")
                            self.data_textbox.insert("0.0", json.dumps(data, indent=4))
                            self.profile_info["data"] = data
                            fastflags.set_data(str(self.name_entry.get()), data)

                        except Exception as e:
                            messagebox.showerror(ProjectData.NAME, f"Unable to import data from \"{os.path.basename(filepath)}\"\n\n{type(e).__name__}: {e}")

                except Exception as e:
                    logger.error(f"Unable to import data, reason: {type(e).__name__}: {e}")
                    messagebox.showerror(ProjectData.NAME, f"Unable to import data!\n\n{type(e).__name__}: {e}")
            

            def _on_export(self) -> None:
                try:
                    data_string: str = self.data_textbox.get("0.0", "end")
                    try:
                        data: dict = json.loads(data_string)
                    except Exception as e:
                        logger.error(f"Unable to export profile, reason:{type(e).__name__}: {e}")
                        messagebox.showerror(ProjectData.NAME, f"Unable to export profile!\n\n{type(e).__name__}: {e}")
                        return
                    
                    if not data:
                        messagebox.showerror(ProjectData.NAME, "No data to export!")
                        return

                    user_profile: str | None = os.getenv("HOME") or os.getenv("USERPROFILE")
                    initial_dir: str = os.path.join(user_profile, "Downloads") if user_profile is not None else os.path.abspath(os.sep)
                    filepath: str | None = filedialog.asksaveasfilename(
                        filetypes=[
                            ("JSON files", "*.json"),
                        ],
                        initialdir=initial_dir,
                        initialfile="ClientAppSettings.json",
                        title="Export profile"
                    )

                    if not filepath:
                        return
                    
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    with open(filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    
                except Exception as e:
                    logger.error(f"Unable to export profile, reason:{type(e).__name__}: {e}")
                    messagebox.showerror(ProjectData.NAME, f"Unable to export profile!\n\n{type(e).__name__}: {e}")
            

            def _on_copy(self) -> None:
                pyperclip.copy(json.dumps(self.profile_info["data"], indent=4))
                messagebox.showinfo(ProjectData.NAME, "Data copied to clipboard!")
        
        
        window = Window(self, profile_info)
        window.show()



    #region Configure FastFlag
    def _create_fastflag_profile(self) -> None:
        profile_info: dict = {
            "name": f"{datetime.now().strftime('%Y-%m-%d@%H:%M:%S.%f')}",
            "description": None,
            "enabled": False,
            "data": {"ExampleFlag": "ExampleValue"}
        }
        fastflags.create(profile_info["name"], profile_info["description"], profile_info["data"])
        self._configure_fastflag_profile(profile_info)
        self._show_fastflags()

    def _rename_fastflag_profile(self, event, profile_info) -> None:
        name: str = profile_info["name"]
        new_name: str = str(event.widget.get())
        if name == new_name:
            return
        
        if not new_name:
            event.widget.delete(0, "end")
            event.widget.insert(0, name)
            return

        try:
            fastflags.set_name(name, new_name)
            profile_info["name"] = new_name
        except fastflags.KeyExistsError as e:
            event.widget.delete(0, "end")
            event.widget.insert(0, name)
            messagebox.showerror(ProjectData.NAME, f"Failed to rename FastFlag profile!\n\n{type(e).__name__}: {e}")

    def _set_fastflag_profile_description(self, event, profile_info) -> None:
        name: str = profile_info["name"]
        description: str | None = profile_info["description"]
        new_description: str | None = str(event.widget.get("0.0", "end"))

        if description == new_description:
            return
        
        if not new_description:
            new_description = None
            # event.widget.delete(0, "end")
            # event.widget.insert(0, description)
            # return
        else:
            new_description = new_description.strip()

        fastflags.set_description(name, new_description)
        profile_info["description"] = new_description
        # self._show_fastflags()

    def _set_fastflag_profile_data(self, event, profile_info) -> None:
        name: str = profile_info["name"]
        data: str | None = profile_info["data"]
        new_data: dict | str = str(event.widget.get("0.0", "end"))

        if data == new_data:
            return
        
        if not new_data:
            new_data = {}
            # event.widget.delete(0, "end")
            # event.widget.insert(0, data)
            # return
        elif isinstance(new_data, dict):
            pass
        else:
            try:
                new_data = json.loads(new_data)
            except Exception as e:
                messagebox.showerror(ProjectData.NAME, f"Failed to update data of FastFlag profile!\n\n{type(e).__name__}: {e}")
                return

        fastflags.set_data(name, new_data)
        profile_info["data"] = new_data
        # self._show_fastflags()

    def _set_fastflag_profile_status(self, name: str, status: bool) -> None:
        try:
            fastflags.set_status(name, status)
        except Exception as e:
            logger.error(f"Failed to update profile status, {type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to update profile status!\n\n{type(e).__name__}: {e}")
    

    def _delete_fastflag_profile(self, name: str) -> None:
        if not messagebox.askokcancel(ProjectData.NAME, f"Are you sure you want to delete this profile:\n\"{name}\"\n\nThis action cannot be undone!"):
            return
        
        try:
            fastflags.remove(name)
            self._show_fastflags()
        except Exception as e:
            logger.error(f"Failed to remove FastFlag profile, {type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to remove FastFlag profile!\n\n{type(e).__name__}: {e}")
    


    # region FastFlag presets
    def _import_fastflag_preset(self) -> None:
        class Window(ctk.CTkToplevel):
            DROPDOWN_PLACEHOLDER: str = "Select an option"

            entry_width: int = 360
            button_size: tuple[int, int] = (44, 44)
            icon_size: tuple[int, int] = (24, 24)
            
            dropdown_name_var = ctk.StringVar(value=DROPDOWN_PLACEHOLDER)
            selected_name_var = ctk.StringVar(value="")
            description_var = ctk.StringVar(value="")

            preset_name: str = ""
            preset_description: str | None = None
            preset_data: dict = {}

            def __init__(self, root, presets: list[dict], *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self.root = root
                self.presets = presets

                if self.root.icon is not None:
                    self.iconbitmap(self.root.icon)
                    self.after(200, lambda: self.iconbitmap(self.root.icon))
                self.title("FastFlag presets")

                self.protocol("WM_DELETE_WINDOW", self._on_close)
                self.bind("<Escape>", lambda _: self._on_close())

                run_icon: str = os.path.join(Directory.root(), "resources", "menu", "common", "run.png")
                if not os.path.isfile(run_icon):
                    try:
                        restore_from_mei(run_icon)
                    except (FileRestoreError, PermissionError, FileNotFoundError):
                        pass

                # Selector frame
                self.selector_frame = ctk.CTkFrame(
                    self,
                    fg_color="transparent"
                )
                self.selector_frame.grid(column=0, row=0, sticky="nsew", padx=32, pady=(32,8))
                # self.selector_frame.grid_columnconfigure(0, weight=1)

                # ctk.CTkLabel(
                #     self.selector_frame,
                #     text="Choose a preset:",
                #     font=self.root.font_bold
                # ).grid(column=0, row=0, sticky="ns", padx=(0,8))

                self.dropdown: ctk.CTkComboBox = ctk.CTkComboBox(
                    self.selector_frame,
                    width=self.entry_width,
                    height=self.button_size[1],
                    variable=self.dropdown_name_var,
                    values=[preset["name"] for preset in self.presets],
                    command=lambda event: self._select_profile()
                )
                self.dropdown.grid(column=0, row=0, sticky="nsw")

                ctk.CTkButton(
                    self.selector_frame,
                    text="",
                    width=self.button_size[0],
                    height=self.button_size[1],
                    image=load_image(
                        light=run_icon,
                        dark=run_icon,
                        size=self.icon_size
                    ),
                    command=self._on_run
                ).grid(column=1, row=0, sticky="nsw", padx=(16,0))

                # Preset info
                info_frame: ctk.CTkFrame = ctk.CTkFrame(
                    self,
                    fg_color="transparent"
                )
                info_frame.grid(column=0, row=1, sticky="nsew", padx=32, pady=(8,32))
                info_frame.grid_columnconfigure(0, weight=1)
                
                # Name
                # name_frame: ctk.CTkFrame = ctk.CTkFrame(
                #     info_frame,
                #     fg_color="transparent"
                # )
                # name_frame.grid(column=0, row=0, sticky="nsew")
                # name_frame.grid_columnconfigure(1, weight=1)

                # ctk.CTkLabel(
                #     name_frame,
                #     text="Name: ",
                #     anchor="w",
                #     justify="left"
                # ).grid(column=0, row=0, sticky="nsew")
                # ctk.CTkLabel(
                #     name_frame,
                #     textvariable=self.selected_name_var,
                #     anchor="w",
                #     justify="left"
                # ).grid(column=1, row=0, sticky="nsew")

                # Description
                description_frame: ctk.CTkFrame = ctk.CTkFrame(
                    info_frame,
                    fg_color="transparent"
                )
                description_frame.grid(column=0, row=0, sticky="nsew")
                description_frame.grid_columnconfigure(1, weight=1)

                ctk.CTkLabel(
                    description_frame,
                    text="Description: ",
                    anchor="w",
                    justify="left",
                    font=self.root.font_13_bold
                ).grid(column=0, row=1, sticky="nsew")
                ctk.CTkLabel(
                    description_frame,
                    textvariable=self.description_var,
                    anchor="w",
                    justify="left",
                    font=self.root.font_13
                ).grid(column=1, row=1, sticky="nsew")


                self.update_idletasks()
                width = self.winfo_reqwidth()
                height = self.winfo_reqheight()
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()
                x = (screen_width // 2) - (width // 2)
                y = (screen_height // 2) - (height // 2)
                self.geometry(f"{width}x{height}+{x}+{y}")
                self.resizable(False, False)
            

            def _select_profile(self) -> None:
                profile_name: str = self.dropdown_name_var.get()
                for preset in self.presets:
                    if preset["name"] == profile_name:
                        description: str | None = preset.get("description")
                        
                        self.selected_name_var.set(profile_name)
                        if description is not None:
                            self.description_var.set(description)
                        else:
                            self.description_var.set("")
                        self.preset_name = profile_name
                        self.preset_description = description
                        self.preset_data = preset["data"]
                
                self.update_idletasks()
                width = self.winfo_reqwidth()
                height = self.winfo_reqheight()
                self.geometry(f"{width}x{height}")

                
            def show(self) -> None:
                self.focus()
                self.grab_set()
                self.wait_window()

            
            def _on_close(self) -> None:
                self.grab_release()
                self.destroy()
            

            def _on_run(self) -> None:
                if not self.selected_name_var:
                    return

                if fastflags.get(self.preset_name) != {}:
                    if messagebox.askokcancel(ProjectData.NAME, "Another profile with the same name already exists!\nDo you wish to overwrite it?"):
                        fastflags.remove(self.preset_name)
                    else:
                        return

                try:
                    fastflags.create(
                        self.preset_name,
                        self.preset_description,
                        self.preset_data
                    )
                except Exception as e:
                    messagebox.showerror(f"Failed to create profile!\n\n{type(e).__name__}: {e}")
                    return
                
                self._on_close()

        try:
            respose: Response = request.get(GitHubApi.fastflag_presets(), cache=True)
            data: list[dict] = respose.json()
        except (RequestError, KeyError) as e:
            logger.error(f"Failed to load FastFlag presets, {type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to load FastFlag presets!\n\n{type(e).__name__}: {e}")
            return
        
        if not data:
            messagebox.showwarning("Failed to load FastFlag presets!\nNo presets found!")
            return

        window = Window(self, data)
        window.show()

        # if profile.exists():
        #    ask_permission() to overwrite_profile()
        #    else return
        # overwrite_profile()
        
        self._show_fastflags()
    


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
                text="Community mods",
                font=self.font_title,
                anchor="w"
            ).grid(column=0, row=0, sticky="nsew")

            ctk.CTkLabel(
                frame,
                text="Download mods with the press of a button",
                font=self.font_large,
                anchor="w"
            ).grid(column=0, row=1, sticky="nsew")
        
        def load_content() -> None:
            pass

        self.active_section = "marketplace"
        destroy()
        load_header()
        load_content()
    


    # region Integrations
    def _show_integrations(self) -> None:
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
                text="Integrations",
                font=self.font_title,
                anchor="w"
            ).grid(column=0, row=0, sticky="nsew")

            ctk.CTkLabel(
                frame,
                text="Manage integrations",
                font=self.font_large,
                anchor="w"
            ).grid(column=0, row=1, sticky="nsew")
        
        def load_content() -> None:
            pass

        self.active_section = "integrations"
        destroy()
        load_header()
        load_content()
    


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
        
        def load_content() -> None:
            pass

        self.active_section = "settings"
        destroy()
        load_header()
        load_content()
    


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
            frame.grid_columnconfigure(0, weight=1)
            frame.grid(column=0, row=0, sticky="nsew")

            ctk.CTkLabel(
                frame,
                text="About",
                font=self.font_title,
                anchor="w"
            ).grid(column=0, row=0, sticky="nsew")

            ctk.CTkLabel(
                frame,
                text=ProjectData.DESCRIPTION,
                font=self.font_large,
                anchor="w"
            ).grid(column=0, row=1, sticky="nsew")
        
        def load_content() -> None:
            pass

        self.active_section = "about"
        destroy()
        load_header()
        load_content()