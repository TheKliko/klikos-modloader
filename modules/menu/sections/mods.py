from pathlib import Path
import re
from tkinter import messagebox
from _tkinter import TclError

from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image
from modules.config import mods
from modules.info import ProjectData

from ..commands import add_mods, open_mods_folder, add_mods, remove_mod, rename_mod
from ..popup_windows.font_import_window import FontImportWindow

import customtkinter as ctk


class ModsSection:
    class Constants:
        SECTION_TITLE: str = "Mods"
        SECTION_DESCRIPTION: str = "Manage your mods"
        MOD_ENTRY_INNER_PADDING: int = 4
        MOD_ENTRY_OUTER_PADDING: int = 12
        MOD_ENTRY_GAP: int = 8
    
    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont


    root: ctk.CTk
    font_import_window: ctk.CTkToplevel
    container: ctk.CTkScrollableFrame


    def __init__(self, root: ctk.CTk, container: ctk.CTkScrollableFrame, font_import_window: FontImportWindow) -> None:
        self.root = root
        self.container = container
        self.font_import_window = font_import_window
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
        frame.grid(column=0, row=0, sticky="nsew", pady=(0,16), padx=(0,4))

        ctk.CTkLabel(frame, text=self.Constants.SECTION_TITLE, anchor="w", font=self.Fonts.title).grid(column=0, row=0, sticky="nsew")
        ctk.CTkLabel(frame, text=self.Constants.SECTION_DESCRIPTION, anchor="w", font=self.Fonts.large).grid(column=0, row=1, sticky="nsew")

        buttons: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
        buttons.grid(column=0, row=2, sticky="nsw", pady=(8,0))

        package_icon: Path = (Directory.RESOURCES / "menu" / "common" / "package").with_suffix(".png")
        if not package_icon.is_file():
            restore_from_meipass(package_icon)
        package_image = load_image(package_icon)

        folder_icon: Path = (Directory.RESOURCES / "menu" / "common" / "folder").with_suffix(".png")
        if not folder_icon.is_file():
            restore_from_meipass(folder_icon)
        folder_image = load_image(folder_icon)

        font_icon: Path = (Directory.RESOURCES / "menu" / "common" / "font").with_suffix(".png")
        if not font_icon.is_file():
            restore_from_meipass(font_icon)
        font_image = load_image(font_icon)

        ctk.CTkButton(buttons, text="Add mods", image=package_image, command=self._add_mods, width=1, anchor="w", compound=ctk.LEFT).grid(column=0, row=0, sticky="nsw")
        ctk.CTkButton(buttons, text="Open mods folder", image=folder_image, command=open_mods_folder, width=1, anchor="w", compound=ctk.LEFT).grid(column=1, row=0, sticky="nsw", padx=(8,0))
        ctk.CTkButton(buttons, text="Add font", image=font_image, command=self._add_font_mod, width=1, anchor="w", compound=ctk.LEFT).grid(column=2, row=0, sticky="nsw", padx=(8,0))
    # endregion


    # region content
    def _load_content(self) -> None:
        configured_mods: list[dict] = mods.read_file()

        container: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=0, row=1, sticky="nsew", padx=(0,4))

        if not Directory.MODS.is_dir():
            Directory.MODS.mkdir(parents=True, exist_ok=True)

        all_mods: list[dict] = [
            mod for mod in configured_mods
            if (Directory.MODS / mod["name"]).is_dir()
        ] + [
            {
                "name": mod.name,
                "enabled": False,
                "priority": 0
            }
            for mod in Directory.MODS.iterdir()
            if mod.name not in [mod.get("name") for mod in configured_mods]
            or not mod.is_dir()
        ]

        if not all_mods:
            not_found_icon: Path = (Directory.RESOURCES / "menu" / "large" / "file-not-found").with_suffix(".png")
            if not not_found_icon.is_file():
                restore_from_meipass(not_found_icon)
            not_found_image = load_image(not_found_icon, size=(96,96))
            
            error_frame: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
            error_frame.place(anchor="c", relx=.5, rely=.5)
            ctk.CTkLabel(error_frame, image=not_found_image, text="").grid(column=0, row=0)
            ctk.CTkLabel(error_frame, text="No mods found!", font=self.Fonts.title).grid(column=1, row=0, sticky="w", padx=(8,0))
            
            return

        bin_icon: Path = (Directory.RESOURCES / "menu" / "common" / "bin").with_suffix(".png")
        if not bin_icon.is_file():
            restore_from_meipass(bin_icon)
        bin_image = load_image(bin_icon)

        for i, mod in enumerate(all_mods):
            try:
                name: str = mod["name"]
            except KeyError:
                continue
            enabled: bool = mod.get("enabled", False)
            priority: int = mod.get("priority", 0)
            enabled_studio: bool = mod.get("enabled_studio", False)

            mod_info: dict = {
                "name": name,
                "enabled": enabled,
                "enabled_studio": enabled_studio,
                "priority": priority
            }
            
            frame: ctk.CTkFrame = ctk.CTkFrame(container)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid(column=0, row=i, sticky="nsew", pady=0 if i == 0 else (self.Constants.MOD_ENTRY_GAP,0))

            # Delete button
            ctk.CTkButton(
                frame, image=bin_image, width=1, height=40, text="", anchor="w", compound=ctk.LEFT,
                command=lambda mod_info=mod_info: self._remove_mod(mod_info)
            ).grid(column=0, row=0, sticky="w", padx=(self.Constants.MOD_ENTRY_OUTER_PADDING, self.Constants.MOD_ENTRY_INNER_PADDING), pady=self.Constants.MOD_ENTRY_OUTER_PADDING)

            # Name label
            name_frame: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
            name_frame.grid_columnconfigure(0, weight=1)
            name_frame.grid(column=1, row=0, sticky="ew", padx=self.Constants.MOD_ENTRY_INNER_PADDING, pady=self.Constants.MOD_ENTRY_OUTER_PADDING)
            
            entry: ctk.CTkEntry = ctk.CTkEntry(
                name_frame, width=256, height=40, validate="key",
                validatecommand=(self.root.register(lambda value: not re.search(r'[\\/:*?"<>|]', value)), "%P")
            )
            entry.insert("end", name)
            entry.bind("<Return>", lambda _: self.root.focus())
            entry.bind("<Control-s>", lambda _: self.root.focus())
            entry.bind("<FocusOut>", lambda event, mod_info=mod_info: self._rename_mod(event, mod_info))
            entry.grid(column=0, row=0, sticky="ew")

            # logo (maybe)
            # logo: Path = Directory.MODS / name / "logo.png"
            # if logo.is_file():
            #     ctk.CTkLabel(
            #         name_frame, text="", width=32, height=32, fg_color="transparent",
            #         image=load_image(logo, size=(32,32))
            #     ).grid(column=1, row=0, sticky="w", padx=(4,0))

            # Mod priority
            priority_frame: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
            priority_frame.grid(column=2, row=0, sticky="ew", padx=self.Constants.MOD_ENTRY_OUTER_PADDING, pady=self.Constants.MOD_ENTRY_OUTER_PADDING)
            ctk.CTkLabel(priority_frame, text="Load order: ", anchor="e").grid(column=0, row=0, sticky="ew")
            entry = ctk.CTkEntry(
                priority_frame, width=40, height=40, validate="key",
                validatecommand=(self.root.register(lambda value: value.isdigit() or value == ""), '%P')
            )
            entry.insert("end", str(priority))
            entry.bind("<Return>", lambda _: self.root.focus())
            entry.bind("<Control-s>", lambda _: self.root.focus())
            entry.bind("<FocusOut>", lambda event, mod_info=mod_info: self._set_mod_priority(event, mod_info))
            entry.grid(column=1, row=0, sticky="ew")

            # Mod status
            status_frame: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
            status_frame.grid(column=3, row=0, sticky="ew", padx=(self.Constants.MOD_ENTRY_INNER_PADDING, self.Constants.MOD_ENTRY_OUTER_PADDING), pady=self.Constants.MOD_ENTRY_OUTER_PADDING)

            player_var: ctk.BooleanVar = ctk.BooleanVar(value=enabled)
            player_switch_frame: ctk.CTkFrame = ctk.CTkFrame(status_frame, fg_color="transparent")
            player_switch_frame.grid(column=0, row=0, sticky="e", padx=(0, self.Constants.MOD_ENTRY_INNER_PADDING))

            ctk.CTkLabel(player_switch_frame, text="Player", anchor="e").grid(column=0, row=0, sticky="e")
            ctk.CTkSwitch(
                player_switch_frame, text="", width=48, variable=player_var, onvalue=True, offvalue=False,
                command=lambda mod_info=mod_info, var=player_var: self._set_mod_status(var.get(), mod_info)
            ).grid(column=1, row=0, sticky="e", padx=(8, 0))

            studio_var: ctk.BooleanVar = ctk.BooleanVar(value=enabled_studio)
            studio_switch_frame: ctk.CTkFrame = ctk.CTkFrame(status_frame, fg_color="transparent")
            studio_switch_frame.grid(column=1, row=0, sticky="e")
            
            ctk.CTkLabel(studio_switch_frame, text="Studio", anchor="e").grid(column=0, row=0, sticky="e")
            ctk.CTkSwitch(
                studio_switch_frame, text="", width=48, variable=studio_var, onvalue=True, offvalue=False,
                command=lambda mod_info=mod_info, var=studio_var: self._set_mod_status_studio(var.get(), mod_info)
            ).grid(column=1, row=0, sticky="e", padx=(8, 0))
    # endregion


    # region functions
    def _add_mods(self) -> None:
        success: bool = add_mods()
        if success:
            self.show()

        
    def _add_font_mod(self) -> None:
        self.font_import_window.show()


    def _remove_mod(self, mod_info: dict) -> None:
        if messagebox.askokcancel(ProjectData.NAME, "Are you sure you want to remove this mod?\nThis action cannot be undone!"):
            remove_mod(mod_info["name"])
            self.show()

    
    def _rename_mod(self, event, mod_info: dict) -> None:
        mod: str = mod_info["name"]
        new: str = str(event.widget.get())

        if mod == new:
            return

        if not new:
            event.widget.delete(0, "end")
            event.widget.insert(0, mod)
            return
        
        if new in [path.name for path in Directory.MODS.iterdir()]:
            messagebox.showerror(ProjectData.NAME, "Another mod with the same name already exists!")
            event.widget.delete(0, "end")
            event.widget.insert(0, mod)
            return

        rename_mod(mod, new)
        mod_info["name"] = new

    
    def _set_mod_priority(self, event, mod_info: dict) -> None:
        mod: str = mod_info["name"]
        old: int = mod_info.get("priority", 0)
        try:
            new: int = int(event.widget.get())
        except ValueError:
            event.widget.delete(0, "end")
            event.widget.insert(0, str(old))
            return

        if old == new:
            return

        if not new and new != 0:
            event.widget.delete(0, "end")
            event.widget.insert(0, str(old))
            return

        mods.set_priority(mod, new)
        mod_info["priority"] = new

    
    def _set_mod_status(self, new: bool, mod_info: dict) -> None:
        mod: str = mod_info["name"]
        old: bool = mod_info.get("enabled", False)

        if old == new:
            return

        mods.set_enabled(mod, new)
        mod_info["enabled"] = new

    
    def _set_mod_status_studio(self, new: bool, mod_info: dict) -> None:
        mod: str = mod_info["name"]
        old: bool = mod_info.get("enabled_studio", False)

        if old == new:
            return

        mods.set_enabled_studio(mod, new)
        mod_info["enabled_studio"] = new
    # endregion