import os
import sys
import shutil
import json
from typing import Callable, Literal

from modules.logger import logger
from modules.info import ProjectData
from modules.filesystem import Directory
from modules import filesystem
from modules.interface.images import load_image
from modules.functions.restore_from_mei import restore_from_mei, FileRestoreError
from modules.functions.config import mods

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
            # button_frame.grid_columnconfigure(2, weight=1)

            package_icon: str = os.path.join(Directory.root(), "resources", "menu", "mods", "package.png")
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

            folder_icon: str = os.path.join(Directory.root(), "resources", "menu", "mods", "folder.png")
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

            font_icon: str = os.path.join(Directory.root(), "resources", "menu", "mods", "font.png")
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

            if installed_mods:
                frame: ctk.CTkFrame = ctk.CTkFrame(
                    self.content,
                    fg_color="transparent"
                )
                frame.grid(column=0, row=1, sticky="nsew")
                for i, mod in enumerate(installed_mods):
                    is_configured: bool = mod in configured_mods
                    if is_configured:
                        data: dict = mods.get(mod)
                        priority: int = data["priority"]
                        enabled: bool = data["enabled"]
                    else:
                        priority = 0
                        enabled = False

                    mod_frame: ctk.CTkFrame = ctk.CTkFrame(
                        frame
                    )
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
                        command=lambda: self._delete_mod(
                            name=mod
                        )
                    ).grid(column=0, row=0, rowspan=2, padx=16, pady=16)

                    # Load order frame
                    load_order_frame: ctk.CTkFrame = ctk.CTkFrame(
                        mod_frame,
                        fg_color="transparent"
                    )
                    load_order_frame.grid(column=2, row=0, rowspan=2, padx=(16,32), pady=16)

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
                    entry.bind("<FocusOut>", lambda event: self._set_mod_priority(event, mod))
                    entry.grid(column=1, row=0, sticky="nsew", padx=8)

                    switch: ctk.CTkSwitch = ctk.CTkSwitch(
                        frame,
                        width=48,
                        height=24,
                        text="",
                        onvalue=True,
                        offvalue=False,
                        command=lambda: self._set_mod_status(mod, switch.get())
                    )
                    switch.grid(column=3, row=0, rowspan=2, sticky="ew", padx=32, pady=32)


        self.active_section = "mods"
        destroy()
        load_header()
        load_content()
    


    # region Configure mods
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
                logger.error(f"Failed to import mod: {mod_name}\n{type(e).__name__}: {e}")
                messagebox.showerror(ProjectData.NAME, f"Failed to import mod: {mod_name}\n{type(e).__name__}: {e}")

        self._show_mods()
    
    def _create_font_mod(self) -> None:
        # region TODO: font mods
        # ctk top level
        # either from file or gogole fonts url
        pass
        self._show_mods()
    
    def _set_mod_status(self, name: str, status: bool) -> None:
        try:
            mods.set_status(name, status)
        except Exception as e:
            logger.error(f"Failed to update mod status\n{type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to update mod status\n{type(e).__name__}: {e}")
    
    def _set_mod_priority(self, event, name: str) -> None:
        try:
            priority: int = int(event.widget.get())
        except Exception as e:
            logger.error(f"Failed to update mod priority\n{type(e).__name__}: {e}")
            event.widget.delete(0, "end")
            event.widget.insert(0, str(mods.get(name).get("priority", mods.FORMAT["priority"])))
            return

        try:
            mods.set_priority(name, priority)
        except Exception as e:
            logger.error(f"Failed to update mod priority\n{type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to update mod priority\n{type(e).__name__}: {e}")
    
    def _rename_mod(self, name: str, new_name: str) -> None:
        if name == new_name:
            return

        mods_directory: str = Directory.mods()
        try:
            os.rename(os.path.join(mods_directory, name), os.path.join(mods_directory, new_name))
        except Exception as e:
            logger.error(f"Failed to rename mod \"{name}\"\n{type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to rename mod \"{name}\"\n{type(e).__name__}: {e}")
            return

        mods.set_name(name, new_name)
        self._show_mods()
    
    def _delete_mod(self, name: str) -> None:
        if not messagebox.askokcancel(ProjectData.NAME, f"Are you sure you want to delete this mod: \"{name}\"\nThis action cannot be undone!"):
            return

        try:
            filesystem.remove(os.path.join(Directory.mods(), name))
        except Exception as e:
            logger.error(f"Failed to delete mod \"{name}\"\n{type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to delete mod \"{name}\"\n{type(e).__name__}: {e}")
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

        self.active_section = "fastflags"
        destroy()
        load_header()
    


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

        self.active_section = "marketplace"
        destroy()
        load_header()
    


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

        self.active_section = "integrations"
        destroy()
        load_header()
    


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

        self.active_section = "settings"
        destroy()
        load_header()
    


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

        self.active_section = "about"
        destroy()
        load_header()