from pathlib import Path
from typing import Callable, Literal
from tkinter import messagebox, filedialog
import json

from modules import Logger
from modules.info import ProjectData
from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image
from modules.config import fastflags

import customtkinter as ctk
import pyperclip


class FastFlagConfigurationSection:
    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont


    root: ctk.CTk
    container: ctk.CTkScrollableFrame
    name_var: ctk.StringVar
    description_var: ctk.StringVar
    return_command: Callable
    profile_info: dict


    def __init__(self, root: ctk.CTk, container: ctk.CTkScrollableFrame) -> None:
        self.root = root
        self.container = container
        self.name_var = ctk.StringVar()
        self.description_var = ctk.StringVar()
        self.data_var = ctk.StringVar()
        self.Fonts.title = ctk.CTkFont(size=20, weight="bold")
        self.Fonts.large = ctk.CTkFont(size=16)
    

    def set_return_command(self, return_command: Callable) -> None:
        self.return_command = return_command


    def show(self, profile_info: dict) -> None:
        self.name_var.set(profile_info["name"])
        self.description_var.set(profile_info["description"] or "No description found")
        self.profile_info = profile_info
        self.data_var.set(json.dumps(profile_info["data"], indent=4))

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

        ctk.CTkLabel(frame, textvariable=self.name_var, anchor="w", font=self.Fonts.title).grid(column=0, row=0, sticky="nsew")
        ctk.CTkLabel(frame, textvariable=self.description_var, anchor="w", font=self.Fonts.large).grid(column=0, row=1, sticky="nsew")

        buttons: ctk.CTkFrame = ctk.CTkFrame(frame, fg_color="transparent")
        buttons.grid(column=0, row=2, sticky="nsw", pady=(8,0))

        return_icon: Path = (Directory.RESOURCES / "menu" / "common" / "return").with_suffix(".png")
        if not return_icon.is_file():
            restore_from_meipass(return_icon)
        return_image = load_image(return_icon)

        pencil_icon: Path = (Directory.RESOURCES / "menu" / "common" / "pencil").with_suffix(".png")
        if not pencil_icon.is_file():
            restore_from_meipass(pencil_icon)
        pencil_image = load_image(pencil_icon)

        import_icon: Path = (Directory.RESOURCES / "menu" / "common" / "import").with_suffix(".png")
        if not import_icon.is_file():
            restore_from_meipass(import_icon)
        import_image = load_image(import_icon)

        export_icon: Path = (Directory.RESOURCES / "menu" / "common" / "export").with_suffix(".png")
        if not export_icon.is_file():
            restore_from_meipass(export_icon)
        export_image = load_image(export_icon)

        clipboard_icon: Path = (Directory.RESOURCES / "menu" / "common" / "clipboard").with_suffix(".png")
        if not clipboard_icon.is_file():
            restore_from_meipass(clipboard_icon)
        clipboard_image = load_image(clipboard_icon)
        
        button_row_1: ctk.CTkFrame = ctk.CTkFrame(buttons, fg_color="transparent")
        button_row_1.grid(column=0, row=0, sticky="nw")
        ctk.CTkButton(button_row_1, text="Go back", image=return_image, command=self.return_command, width=1, anchor="w", compound=ctk.LEFT).grid(column=0, row=0, sticky="nsw")
        ctk.CTkButton(button_row_1, text="Change name", image=pencil_image, command=self._change_profile_name, width=1, anchor="w", compound=ctk.LEFT).grid(column=1, row=0, sticky="nsw", padx=(8,0))
        ctk.CTkButton(button_row_1, text="Change description", image=pencil_image, command=self._change_profile_description, width=1, anchor="w", compound=ctk.LEFT).grid(column=2, row=0, sticky="nsw", padx=(8,0))
        ctk.CTkButton(button_row_1, text="Import data", image=import_image, command=self._import_data, width=1, anchor="w", compound=ctk.LEFT).grid(column=3, row=0, sticky="nsw", padx=(8,0))
        ctk.CTkButton(button_row_1, text="Export data", image=export_image, command=self._export_data, width=1, anchor="w", compound=ctk.LEFT).grid(column=4, row=0, sticky="nsw", padx=(8,0))
        
        button_row_2: ctk.CTkFrame = ctk.CTkFrame(buttons, fg_color="transparent")
        button_row_2.grid(column=0, row=1, sticky="nw", pady=(8, 0))
        ctk.CTkButton(button_row_2, text="Copy to clipboard", image=clipboard_image, command=self._copy_data, width=1, anchor="w", compound=ctk.LEFT).grid(column=0, row=0, sticky="nsw")
    # endregion


    # region content
    # def _load_content(self) -> None:
    #     container: ctk.CTkFrame = ctk.CTkFrame(self.container)
    #     container.grid_columnconfigure(0, weight=1)
    #     container.grid(column=0, row=3, sticky="nsew")

    #     title: ctk.CTkFrame = ctk.CTkFrame(container, corner_radius=0)
    #     title.grid_columnconfigure(0, weight=1)
    #     title.grid_columnconfigure(1, weight=1)
    #     title.grid(column=0, row=0, sticky="ew")
    #     ctk.CTkLabel(title, text="Flag", anchor="w").grid(column=0, row=0, sticky="w", padx=(8, 0))
    #     ctk.CTkLabel(title, text="Value", anchor="w").grid(column=1, row=0, sticky="w", padx=(8, 0))

    #     content: ctk.CTkFrame = ctk.CTkFrame(container, corner_radius=0)
    #     content.grid_columnconfigure(0, weight=1)
    #     content.grid_columnconfigure(1, weight=1)
    #     content.grid(column=0, row=1, sticky="ew")

    #     for i, (flag, value) in enumerate(self.profile_info["data"].items()):
    #         flag_variable: ctk.StringVar = ctk.StringVar(value=str(flag))
    #         value_variable: ctk.StringVar = ctk.StringVar(value=str(value))
    #         ctk.CTkEntry(content, textvariable=flag_variable).grid(column=0, row=i, sticky="ew", padx=8, pady=8)
    #         ctk.CTkEntry(content, textvariable=value_variable).grid(column=1, row=i, sticky="ew", padx=8, pady=8)
    # endregion


    # region content
    def _load_content(self) -> None:
        container: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=0, row=3, sticky="nsew", padx=(0, 4))

        textbox: ctk.CTkTextbox = ctk.CTkTextbox(container, wrap="none", text_color="#9cdcfe", height=self.root.Constants.HEIGHT - 172)
        textbox.insert("0.0", json.dumps(self.profile_info["data"], indent=4))
        textbox.bind("<Return>", lambda _: self.root.focus())
        textbox.bind("<Control-s>", lambda _: self.root.focus())
        textbox.bind("<FocusOut>", self._update_profile_data)
        textbox.grid(column=0, row=0, sticky="nsew")
    # endregion


    # region functions
    def _copy_data(self) -> None:
        pyperclip.copy(json.dumps(self.profile_info["data"], indent=4))
        messagebox.showinfo(ProjectData.NAME, "Data copied to clipboard!")
    

    def _change_profile_name(self) -> None:
        dialog: ctk.CTkInputDialog = ctk.CTkInputDialog(text="Profile name:", title=ProjectData.NAME)
        response: str = dialog.get_input()

        if not response:
            return
        
        if response in [item.get("name") for item in fastflags.read_file()]:
            messagebox.showerror(ProjectData.NAME, "Another profile with the same name already exists!")
            return
        
        fastflags.set_name(self.profile_info["name"], response)
        self.profile_info["name"] = response
        self.name_var.set(response)
    

    def _change_profile_description(self) -> None:
        dialog: ctk.CTkInputDialog = ctk.CTkInputDialog(text="Profile name:", title=ProjectData.NAME)
        response: str = dialog.get_input()

        if response is None:
            return
        
        if not response:
            fastflags.set_description(self.profile_info["name"], None)
            self.profile_info["description"] = None
            self.description_var.set("No description found")
            return
        
        fastflags.set_description(self.profile_info["name"], response)
        self.profile_info["description"] = response
        self.description_var.set(response)

        
    def _export_data(self) -> None:
        try:
            initial_dir: Path = Path().home()
            if (initial_dir / "Downloads").is_dir():
                initial_dir = initial_dir / "Downloads"

            filepath: str | Literal[''] = filedialog.askopenfilename(
                title=f"{ProjectData.NAME} | Import mods", initialdir=initial_dir,
                filetypes=[("JSON Files", "*.json")],
                initialfile="ClientAppSettings.json"
            )

            if filepath == '':
                return
            
            with open(filepath, "w") as file:
                json.dump(self.profile_info["data"], file, indent=4)
            messagebox.showinfo(ProjectData.NAME, "FastFlag profile exported succesfully!")

        except Exception as e:
            Logger.error(f"Failed to export FastFlag profile! {type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Something went wrong!\n{type(e).__name__}: {e}")


    def _import_data(self) -> None:
        try:
            initial_dir: Path = Path().home()
            if (initial_dir / "Downloads").is_dir():
                initial_dir = initial_dir / "Downloads"

            filepath: str | Literal[''] = filedialog.askopenfilename(
                title=f"{ProjectData.NAME} | Import mods", initialdir=initial_dir,
                filetypes=[("JSON Files", "*.json")],
                initialfile="ClientAppSettings.json"
            )

            if filepath == '':
                return
            
            with open(filepath, "r") as file:
                data: dict = json.load(file)
            self.profile_info.update(data)

        except Exception as e:
            Logger.error(f"Failed to import FastFlag profile! {type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Something went wrong!\n{type(e).__name__}: {e}")
        
        else:
            self.show(self.profile_info)
    

    def _update_profile_data(self, event) -> None:
        try:
            new_data_string: str = event.widget.get()
            new_data: dict = json.loads(new_data_string)
            fastflags.set_data(self.profile_info["name"], new_data)
            self.profile_info["data"] = new_data

        except Exception as e:
            Logger.error(f"Failed to save FastFlag profile! {type(e).__name__}: {e}")
            messagebox.showerror(ProjectData.NAME, f"Failed to save profile!\n{type(e).__name__}: {e}")
    # endregion