from pathlib import Path
from typing import Optional
from tkinter import messagebox

from modules.info import ProjectData
from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image
from modules.config import fastflags

from ..sections.fastflag_configuration import FastFlagConfigurationSection
from ..popup_windows.fastflag_preset_window import FastFlagPresetWindow

import customtkinter as ctk


class FastFlagsSection:
    class Constants:
        SECTION_TITLE: str = "FastFlags"
        SECTION_DESCRIPTION: str = "Manage your FastFlags"
        PROFILE_ENTRY_INNER_PADDING: int = 4
        PROFILE_ENTRY_OUTER_PADDING: int = 12
        PROFILE_ENTRY_GAP: int = 8


    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont


    root: ctk.CTk
    container: ctk.CTkScrollableFrame
    fastflag_configuration_section: FastFlagConfigurationSection
    fastflag_preset_window: FastFlagPresetWindow


    def __init__(self, root: ctk.CTk, container: ctk.CTkScrollableFrame, fastflag_configuration_section: FastFlagConfigurationSection, fastflag_preset_window: FastFlagPresetWindow) -> None:
        self.root = root
        self.container = container
        self.fastflag_configuration_section = fastflag_configuration_section
        self.fastflag_preset_window = fastflag_preset_window
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
        frame.grid(column=0, row=0, sticky="nsew", pady=(0,16))

        ctk.CTkLabel(frame, text=self.Constants.SECTION_TITLE, anchor="w", font=self.Fonts.title).grid(column=0, row=0, sticky="nsew")
        ctk.CTkLabel(frame, text=self.Constants.SECTION_DESCRIPTION, anchor="w", font=self.Fonts.large).grid(column=0, row=1, sticky="nsew")

        buttons: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
        buttons.grid(column=0, row=2, sticky="nsw", pady=(8,0))

        create_icon: Path = (Directory.RESOURCES / "menu" / "common" / "create").with_suffix(".png")
        if not create_icon.is_file():
            restore_from_meipass(create_icon)
        create_image = load_image(create_icon)

        cloud_icon: Path = (Directory.RESOURCES / "menu" / "common" / "cloud").with_suffix(".png")
        if not cloud_icon.is_file():
            restore_from_meipass(cloud_icon)
        cloud_image = load_image(cloud_icon)
        
        ctk.CTkButton(buttons, text="New profile", image=create_image, command=self._new_profile, width=1, anchor="w", compound=ctk.LEFT).grid(column=0, row=0, sticky="nsw")
        ctk.CTkButton(buttons, text="Presets", image=cloud_image, command=self._load_preset, width=1, anchor="w", compound=ctk.LEFT).grid(column=1, row=0, sticky="nsw", padx=(8,0))
    # endregion


    # region content
    def _load_content(self) -> None:
        fastflag_profiles: list[dict] = fastflags.read_file()

        container: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=0, row=1, sticky="nsew", padx=(0,4))

        if not fastflag_profiles:
            no_fastflags_icon: Path = (Directory.RESOURCES / "menu" / "large" / "no-fastflags").with_suffix(".png")
            if not no_fastflags_icon.is_file():
                restore_from_meipass(no_fastflags_icon)
            no_fastflags_image = load_image(no_fastflags_icon, size=(96,96))
            
            error_frame: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
            error_frame.place(anchor="c", relx=.5, rely=.5)
            ctk.CTkLabel(error_frame, image=no_fastflags_image, text="").grid(column=0, row=0)
            ctk.CTkLabel(error_frame, text="No FastFlags found!", font=self.Fonts.title).grid(column=1, row=0, sticky="w", padx=(8,0))
            
            return

        bin_icon: Path = (Directory.RESOURCES / "menu" / "common" / "bin").with_suffix(".png")
        if not bin_icon.is_file():
            restore_from_meipass(bin_icon)
        bin_image = load_image(bin_icon)

        configure_icon: Path = (Directory.RESOURCES / "menu" / "common" / "configure").with_suffix(".png")
        if not configure_icon.is_file():
            restore_from_meipass(configure_icon)
        configure_image = load_image(configure_icon)

        for i, profile in enumerate(fastflag_profiles):
            try:
                name: str = profile["name"]
                data: dict = profile["data"]
            except KeyError:
                continue
            enabled: bool = profile.get("enabled", False)
            enabled_studio: bool = profile.get("enabled_studio", False)
            description: Optional[str] = profile.get("description")

            profile_info: dict = {
                "name": name,
                "description": description,
                "enabled": enabled,
                "enabled_studio": enabled_studio,
                "data": data
            }
            
            frame: ctk.CTkFrame = ctk.CTkFrame(container)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid(column=0, row=i, sticky="nsew", pady=0 if i == 0 else (self.Constants.PROFILE_ENTRY_GAP,0))

            # Delete button
            ctk.CTkButton(
                frame, image=bin_image, width=1, height=40, text="", anchor="w", compound=ctk.LEFT,
                command=lambda profile_info=profile_info: self._remove_profile(profile_info)
            ).grid(column=0, row=0, sticky="w", padx=(self.Constants.PROFILE_ENTRY_OUTER_PADDING, self.Constants.PROFILE_ENTRY_INNER_PADDING), pady=self.Constants.PROFILE_ENTRY_OUTER_PADDING)

            # Name label
            name_frame: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
            name_frame.grid_columnconfigure(0, weight=1)
            name_frame.grid(column=1, row=0, sticky="ew", padx=self.Constants.PROFILE_ENTRY_INNER_PADDING, pady=self.Constants.PROFILE_ENTRY_OUTER_PADDING)
            
            entry: ctk.CTkEntry = ctk.CTkEntry(
                name_frame, width=256, height=40
            )
            entry.insert("end", name)
            entry.bind("<Return>", lambda _: self.root.focus())
            entry.bind("<Control-s>", lambda _: self.root.focus())
            entry.bind("<FocusOut>", lambda event, profile_info=profile_info: self._rename_profile(event, profile_info))
            entry.grid(column=0, row=0, sticky="ew")

            # Configure button
            ctk.CTkButton(
                frame, image=configure_image, text="Configure", width=1, height=40, anchor="w", compound=ctk.LEFT,
                command=lambda profile_info=profile_info: self.fastflag_configuration_section.show(profile_info)
            ).grid(column=2, row=0, sticky="w", padx=self.Constants.PROFILE_ENTRY_OUTER_PADDING, pady=self.Constants.PROFILE_ENTRY_OUTER_PADDING)

            # Mod status
            status_frame: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
            status_frame.grid(column=3, row=0, sticky="ew", padx=(self.Constants.PROFILE_ENTRY_INNER_PADDING, self.Constants.PROFILE_ENTRY_OUTER_PADDING), pady=self.Constants.PROFILE_ENTRY_OUTER_PADDING)

            player_var: ctk.BooleanVar = ctk.BooleanVar(value=enabled)
            player_switch_frame: ctk.CTkFrame = ctk.CTkFrame(status_frame, fg_color="transparent")
            player_switch_frame.grid(column=0, row=0, sticky="e", padx=(0, self.Constants.PROFILE_ENTRY_INNER_PADDING))

            ctk.CTkLabel(player_switch_frame, text="Player", anchor="e").grid(column=0, row=0, sticky="e")
            ctk.CTkSwitch(
                player_switch_frame, text="", width=48, variable=player_var, onvalue=True, offvalue=False,
                command=lambda profile_info=profile_info, var=player_var: self._set_profile_status(var.get(), profile_info)
            ).grid(column=1, row=0, sticky="e", padx=(8, 0))

            studio_var: ctk.BooleanVar = ctk.BooleanVar(value=enabled_studio)
            studio_switch_frame: ctk.CTkFrame = ctk.CTkFrame(status_frame, fg_color="transparent")
            studio_switch_frame.grid(column=1, row=0, sticky="e")

            ctk.CTkLabel(studio_switch_frame, text="Studio", anchor="e").grid(column=0, row=0, sticky="e")
            ctk.CTkSwitch(
                studio_switch_frame, text="", width=48, variable=studio_var, onvalue=True, offvalue=False,
                command=lambda profile_info=profile_info, var=studio_var: self._set_profile_status_studio(var.get(), profile_info)
            ).grid(column=1, row=0, sticky="e", padx=(8, 0))
    # endregion


    # region functions
    def _new_profile(self) -> None:
        dialog: ctk.CTkInputDialog = ctk.CTkInputDialog(text="Profile name:", title=ProjectData.NAME)
        response: str = dialog.get_input()

        if not response:
            return
        
        if response in [item.get("name") for item in fastflags.read_file()]:
            messagebox.showerror(ProjectData.NAME, "Another profile with the same name already exists!")
            return

        fastflags.add_item(response)
        # self.show()

        # Don't refresh the section, go straight to configuring the new profile
        item: dict = fastflags.get_item(response)
        profile_info: dict = {
            "name": item["name"],
            "description": item.get("description"),
            "enabled": item.get("enabled", False),
            "enabled_studio": item.get("enabled_studio", False),
            "data": item.get("data", {})
        }
        self.fastflag_configuration_section.show(profile_info)


    def _remove_profile(self, profile_info: dict) -> None:
        if messagebox.askokcancel(ProjectData.NAME, "Are you sure you want to remove this profile?\nThis action cannot be undone!"):
            fastflags.remove_item(profile_info["name"])
            self.show()


    def _rename_profile(self, event, profile_info: dict) -> None:
        profile: str = profile_info["name"]
        new: str = str(event.widget.get())

        if profile == new:
            return
        
        if not new:
            event.widget.delete(0, "end")
            event.widget.insert(0, profile)
            return
        
        if new in [item.get("name") for item in fastflags.read_file()]:
            messagebox.showerror(ProjectData.NAME, "Another profile with the same name already exists!")
            event.widget.delete(0, "end")
            event.widget.insert(0, profile)
            return
        
        fastflags.set_name(profile, new)
        profile_info["name"] = new

    
    def _set_profile_status(self, new: bool, profile_info: dict) -> None:
        mod: str = profile_info["name"]
        old: bool = profile_info.get("enabled", False)

        if old == new:
            return

        fastflags.set_enabled(mod, new)
        profile_info["enabled"] = new

    
    def _set_profile_status_studio(self, new: bool, profile_info: dict) -> None:
        mod: str = profile_info["name"]
        old: bool = profile_info.get("enabled_studio", False)

        if old == new:
            return

        fastflags.set_enabled_studio(mod, new)
        profile_info["enabled_studio"] = new
    

    def _load_preset(self) -> None:
        self.fastflag_preset_window.show()
    # endregion