from pathlib import Path
from typing import Optional, Callable
from _tkinter import TclError

from modules import Logger
from modules.info import ProjectData
from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image
from modules import request
from modules.request import Response, Api
from modules.config import fastflags

import customtkinter as ctk


class FastFlagPresetWindow(ctk.CTkToplevel):
    class Fonts:
        title: ctk.CTkFont
        bold: ctk.CTkFont


    BUTTON_SIZE: int = 40
    DROPDOWN_RATIO: float = 7.5
    root: ctk.CTk
    on_success: Callable

    presets: dict[str, dict]
    preset_options: list[str]
    presets_loaded: bool = False
    selected_item: str = ""
    dropdown_variable: ctk.StringVar
    description_variable: ctk.StringVar


    def __init__(self, root: ctk.CTk, *args, **kwargs) -> None:
        self.root = root
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._hide)
        self.bind("<Escape>", self._hide)

        # Hide window immediately after it's created. Only show it when needed
        self.withdraw()

        self.Fonts.title = ctk.CTkFont(size=20, weight="bold")
        self.Fonts.bold = ctk.CTkFont(weight="bold")
        self.dropdown_variable = ctk.StringVar()
        self.description_variable = ctk.StringVar(value="No preset selected!")
        
        if not self.root.Constants.FAVICON.is_file():
            restore_from_meipass(self.root.Constants.FAVICON)
        self.iconbitmap(self.root.Constants.FAVICON.resolve())
        self.after(200, lambda: self.iconbitmap(self.root.Constants.FAVICON.resolve()))
        self.title(f"{ProjectData.NAME} | FastFlag presets")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame: ctk.CTkFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.grid(column=0, row=0, sticky="nsew", padx=32, pady=32)

        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        self.geometry(self._get_geometry(width, height))
    

    def set_refresh_function(self, func: Callable) -> None:
        self.on_success = func


    def show(self) -> None:
        self._destroy_content()
        self._load_content()
        self.deiconify()
        # self.geometry(self._get_geometry())
        self.grab_set()
        self.wm_transient(self.root)


    def _get_geometry(self, width: Optional[int] = None, height: Optional[int] = None) -> str:
        root_geometry: str = self.root.winfo_geometry()
        root_size, root_x, root_y = root_geometry.split("+")
        root_width, root_height = map(int, root_size.split("x"))

        self.update_idletasks()
        width = width or self.winfo_width()
        height = height or self.winfo_height()

        x: int = int(root_x) + ((root_width - width) // 2)
        y: int = int(root_y) + ((root_height - height) // 2)

        return f"{width}x{height}+{x}+{y}"
    

    def _hide(self, *args, **kwargs) -> None:
        try:
            self.grab_release()
            self.withdraw()
        except TclError:
            pass
    

    def _destroy_content(self) -> None:
        for widget in self.frame.winfo_children():
            widget.destroy()
    

    def _load_content(self) -> None:
        self._load_presets()
        if not self.presets_loaded:
            no_fastflags_icon: Path = (Directory.RESOURCES / "menu" / "large" / "no-fastflags").with_suffix(".png")
            if not no_fastflags_icon.is_file():
                restore_from_meipass(no_fastflags_icon)
            no_fastflags_image = load_image(no_fastflags_icon, size=(96,96))
            
            error_frame: ctk.CTkFrame = ctk.CTkFrame(self.frame, fg_color="transparent")
            error_frame.grid(column=0, row=0, sticky="nsew")
            ctk.CTkLabel(error_frame, image=no_fastflags_image, text="").grid(column=0, row=0)
            ctk.CTkLabel(error_frame, text="Presets failed to load!", font=self.Fonts.title).grid(column=1, row=0, sticky="w", padx=(8,0))
            
        else:
            dropdown: ctk.CTkComboBox = ctk.CTkComboBox(self.frame, values=self.preset_options, variable=self.dropdown_variable, command=self._update_description, width=int(self.DROPDOWN_RATIO * self.BUTTON_SIZE), height=self.BUTTON_SIZE)
            dropdown.grid(column=0, row=0, sticky="w")

            run_icon: Path = (Directory.RESOURCES / "menu" / "common" / "run").with_suffix(".png")
            if not run_icon.is_file():
                restore_from_meipass(run_icon)
            run_image = load_image(run_icon)
            ctk.CTkButton(self.frame, image=run_image, command=self._run, text="", width=self.BUTTON_SIZE, height=self.BUTTON_SIZE).grid(column=1, row=0, sticky="w", padx=(4,0))

            # Info
            ctk.CTkLabel(self.frame, text="Desription", font=self.Fonts.bold, anchor="w").grid(column=0, row=1, sticky="w", pady=(16,0))
            ctk.CTkEntry(self.frame, textvariable=self.description_variable, state="disabled", width=int(self.DROPDOWN_RATIO * self.BUTTON_SIZE) + self.BUTTON_SIZE + 4).grid(column=0, row=2, sticky="w", columnspan=2)

        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()

        self.geometry(self._get_geometry(width, height))


    def _load_presets(self) -> None:
        self.presets_loaded = False
        try:        
            response: Response = request.get(Api.GitHub.FASTFLAG_PRESETS, attempts=1, cached=True, timeout=(2, 4))
            data: list[dict] = response.json()
            self.presets = {
                item.get("name"): {
                    "name": item.get("name"),
                    "description": item.get("description"),
                    "data": item.get("data")
                }
                for item in data
                if item.get("name") is not None and item.get("data") is not None
            }
            self.preset_options = list(self.presets.keys())
            self.presets_loaded = True
        
        except Exception as e:
            Logger.error(f"FastFlag presets failed to load! {type(e).__name__}: {e}")
            self.presets_loaded = False


    def _update_description(self, event) -> None:
        self.selected_item = self.dropdown_variable.get()
        self.description_variable.set(self.presets[self.selected_item].get("description") or "Description not found")


    def _run(self) -> None:
        if not self.selected_item:
            return

        profile: dict = self.presets[self.selected_item]
        name: str = profile["name"]
        current_enabled: bool | None = None
        current_enabled_studio: bool | None = None

        if name in [item.get("name") for item in fastflags.read_file()]:
            existing_item: dict = fastflags.get_item(name)
            current_enabled = existing_item.get("enabled")
            current_enabled_studio = existing_item.get("enabled_studio")
            fastflags.remove_item(name)

        fastflags.add_item(name, description=profile.get("description"), profile_data=profile["data"])
        
        if current_enabled is not None:
            fastflags.set_enabled(name, current_enabled)
        if current_enabled_studio is not None:
            fastflags.set_enabled_studio(name, current_enabled_studio)

        self._hide()
        self.on_success()