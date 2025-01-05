from pathlib import Path
from typing import Literal
from tkinter import filedialog, messagebox

from modules.info import ProjectData
from modules.config import launch_apps
from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image

import customtkinter as ctk


class LaunchAppsSection:
    class Constants:
        SECTION_TITLE: str = "Launch apps"
        SECTION_DESCRIPTION: str = "Launch other applications when Roblox is launched"
        ENTRY_INNER_PADDING: int = 4
        ENTRY_OUTER_PADDING: int = 12
        ENTRY_GAP: int = 8
    
    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont
        bold: ctk.CTkFont


    root: ctk.CTk
    container: ctk.CTkScrollableFrame


    def __init__(self, root: ctk.CTk, container: ctk.CTkScrollableFrame) -> None:
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

        create_icon: Path = (Directory.RESOURCES / "menu" / "common" / "create").with_suffix(".png")
        if not create_icon.is_file():
            restore_from_meipass(create_icon)
        create_image = load_image(create_icon)

        ctk.CTkButton(buttons, text="New", image=create_image, command=self._new_launch_app, width=1, anchor="w", compound=ctk.LEFT).grid(column=0, row=0, sticky="nsw")
    # endregion


    # region content
    def _load_content(self) -> None:
        configured_apps: list[dict] = launch_apps.read_file()

        container: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=0, row=1, sticky="nsew", padx=(0,4))

        if not configured_apps:
            not_found_icon: Path = (Directory.RESOURCES / "menu" / "large" / "file-not-found").with_suffix(".png")
            if not not_found_icon.is_file():
                restore_from_meipass(not_found_icon)
            not_found_image = load_image(not_found_icon, size=(96,96))
            
            error_frame: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
            error_frame.place(anchor="c", relx=.5, rely=.5)
            ctk.CTkLabel(error_frame, image=not_found_image, text="").grid(column=0, row=0)
            ctk.CTkLabel(error_frame, text="No launch apps found!", font=self.Fonts.title).grid(column=1, row=0, sticky="w", padx=(8,0))
            
            return

        bin_icon: Path = (Directory.RESOURCES / "menu" / "common" / "bin").with_suffix(".png")
        if not bin_icon.is_file():
            restore_from_meipass(bin_icon)
        bin_image = load_image(bin_icon)

        for i, item in enumerate(configured_apps):
            try:
                filepath: str = item["filepath"]
            except KeyError:
                continue
            launch_args: str | None = item.get("launch_args")
            enabled: bool = item.get("enabled", False)
            enabled_studio: bool = item.get("enabled_studio", False)
            filepath_as_path: Path = Path(filepath)
            
            frame: ctk.CTkFrame = ctk.CTkFrame(container)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid(column=0, row=i, sticky="nsew", pady=0 if i == 0 else (self.Constants.ENTRY_GAP,0))

            # Name label
            ctk.CTkLabel(frame, text=filepath_as_path.name, anchor="w", font=self.Fonts.bold).grid(column=0, row=0, columnspan=2, sticky="nw", padx=self.Constants.ENTRY_OUTER_PADDING, pady=(self.Constants.ENTRY_OUTER_PADDING, self.Constants.ENTRY_INNER_PADDING))

            # Delete button
            ctk.CTkButton(
                frame, image=bin_image, width=1, height=40, text="", anchor="w", compound=ctk.LEFT,
                command=lambda key=filepath: self._remove_app(key)
            ).grid(column=0, row=1, sticky="w", padx=(self.Constants.ENTRY_OUTER_PADDING, self.Constants.ENTRY_INNER_PADDING), pady=(0, self.Constants.ENTRY_OUTER_PADDING))

            # Launch args
            args_frame: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
            args_frame.grid_columnconfigure(1, weight=1)
            args_frame.grid(column=1, row=1, sticky="ew", padx=self.Constants.ENTRY_INNER_PADDING, pady=(0, self.Constants.ENTRY_OUTER_PADDING))

            ctk.CTkLabel(args_frame, text="args", anchor="e").grid(column=0, row=0, padx=(0, 4))

            entry: ctk.CTkEntry = ctk.CTkEntry(args_frame, height=40)
            entry.insert("end", launch_args or "")
            entry.bind("<Return>", lambda _: self.root.focus())
            entry.bind("<Control-s>", lambda _: self.root.focus())
            entry.bind("<FocusOut>", lambda event, key=filepath: self._set_args(event, key))
            entry.grid(column=1, row=0, sticky="ew")

            # Status
            status_frame: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
            status_frame.grid(column=2, row=1, sticky="ew", padx=2*self.Constants.ENTRY_INNER_PADDING, pady=(0, self.Constants.ENTRY_OUTER_PADDING))

            player_var: ctk.BooleanVar = ctk.BooleanVar(value=enabled)
            player_switch_frame: ctk.CTkFrame = ctk.CTkFrame(status_frame, fg_color="transparent")
            player_switch_frame.grid(column=0, row=0, sticky="e", padx=(0, self.Constants.ENTRY_INNER_PADDING))

            ctk.CTkLabel(player_switch_frame, text="Roblox Player", anchor="e").grid(column=0, row=0, sticky="e")
            ctk.CTkSwitch(
                player_switch_frame, text="", width=48, variable=player_var, onvalue=True, offvalue=False,
                command=lambda key=filepath, var=player_var: self._set_status(var.get(), key)
            ).grid(column=1, row=0, sticky="e", padx=(self.Constants.ENTRY_INNER_PADDING,0))

            studio_var: ctk.BooleanVar = ctk.BooleanVar(value=enabled_studio)
            studio_switch_frame: ctk.CTkFrame = ctk.CTkFrame(status_frame, fg_color="transparent")
            studio_switch_frame.grid(column=1, row=0, sticky="e")
            
            ctk.CTkLabel(studio_switch_frame, text="Roblox Studio", anchor="e").grid(column=0, row=0, sticky="e")
            ctk.CTkSwitch(
                studio_switch_frame, text="", width=48, variable=studio_var, onvalue=True, offvalue=False,
                command=lambda key=filepath, var=studio_var: self._set_status_studio(var.get(), key)
            ).grid(column=1, row=0, sticky="e", padx=(self.Constants.ENTRY_INNER_PADDING,0))
    # endregion


    # region functions
    def _new_launch_app(self) -> None:
        initial_dir: Path = Path().home()
        if (initial_dir / "Downloads").is_dir():
            initial_dir = initial_dir / "Downloads"

        file: str | Literal[''] = filedialog.askopenfilename(
            title=f"{ProjectData.NAME} | New Launch App", initialdir=initial_dir,
            filetypes=[("All Files", "*.*")]
        )

        if not file:
            return
        
        filepath: Path = Path(file)

        # if filepath.name in [item.get("name") for item in launch_apps.read_file()]:
        #     messagebox.showerror(ProjectData.NAME, "Another launch app with the same name already exists!")
        #     return
        
        if str(filepath.resolve()) in [item.get("filepath") for item in launch_apps.read_file()]:
            messagebox.showerror(ProjectData.NAME, "Another launch app for the same file already exists!")
            return
        
        launch_apps.add_item(filepath)

        self.show()


    def _remove_app(self, key: str) -> None:
        launch_apps.remove_item(key)
        self.show()

    
    def _set_status(self, new: bool, key: str) -> None:
        launch_apps.set_enabled(key, new)

    
    def _set_status_studio(self, new: bool, key: str) -> None:
        launch_apps.set_enabled_studio(key, new)

    
    def _set_args(self, event, key: str) -> None:
        new: str | None = str(event.widget.get())

        if not new:
            new = None

        launch_apps.set_args(key, new)
    # endregion