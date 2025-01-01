from pathlib import Path
import re
from tkinter import colorchooser, messagebox
from threading import Thread

from modules.info import ProjectData
from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image
from modules import mod_generator

import customtkinter as ctk


class ModGeneratorSection:
    class Constants:
        SECTION_TITLE: str = "Mod Generator [BETA]"
        SECTION_DISCLAIMER: str = "Disclaimer: this tool only generates the ImageSets, it does not generate a complete mod"
    
    class Fonts:
        title: ctk.CTkFont
        large: ctk.CTkFont
        bold: ctk.CTkFont


    root: ctk.CTk
    container: ctk.CTkScrollableFrame
    mod_name_entry: ctk.CTkEntry
    color_variable: ctk.StringVar
    progress_variable: ctk.StringVar
    is_running: bool = False


    def __init__(self, root: ctk.CTk, container: ctk.CTkScrollableFrame) -> None:
        self.root = root
        self.container = container
        self.Fonts.title = ctk.CTkFont(size=20, weight="bold")
        self.Fonts.large = ctk.CTkFont(size=16)
        self.Fonts.bold = ctk.CTkFont(weight="bold")
        
        self.color_variable = ctk.StringVar(value="None")
        self.progress_variable = ctk.StringVar()


    def show(self) -> None:
        self.color_variable.set("None")
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
        ctk.CTkLabel(frame, text=self.Constants.SECTION_DISCLAIMER, anchor="w", font=self.Fonts.large).grid(column=0, row=1, sticky="nsew")
    # endregion


    # region content
    def _load_content(self) -> None:
        container: ctk.CTkFrame = ctk.CTkFrame(self.container, fg_color="transparent")
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=0, row=1, sticky="nsew", padx=(0,4))

        # name input
        name_frame: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
        name_frame.grid(column=0, row=0, sticky="nsew")
        ctk.CTkLabel(name_frame, text="Name:", anchor="w", font=self.Fonts.bold).grid(column=0, row=0, sticky="nw")
        self.mod_name_entry = ctk.CTkEntry(
            name_frame, width=256, height=40, validate="key",
            validatecommand=(self.root.register(lambda value: not re.search(r'[\\/:*?"<>|]', value)), "%P")
        )
        self.mod_name_entry.grid(column=0, row=1, sticky="nw")
        
        # color input
        color_frame: ctk.CTkFrame = ctk.CTkFrame(container, fg_color="transparent")
        color_frame.grid(column=0, row=1, sticky="nsew", pady=(16, 32))
        ctk.CTkLabel(color_frame, text="Color:", anchor="w", font=self.Fonts.bold).grid(column=0, row=0, sticky="w")

        color_preview_frame: ctk.CTkFrame = ctk.CTkFrame(color_frame, fg_color="transparent")
        color_preview_frame.grid(column=0, row=1, sticky="nsew")
        self.color_visualizer = ctk.CTkFrame(color_preview_frame, width=40, height=40)
        self.color_visualizer.grid(column=0, row=0, sticky="nw")
        
        ctk.CTkLabel(color_preview_frame, textvariable=self.color_variable, anchor="w").grid(column=1, row=0, sticky="w", padx=(4, 0))
        
        color_select_icon: Path = (Directory.RESOURCES / "menu" / "common" / "color-select").with_suffix(".png")
        if not color_select_icon.is_file():
            restore_from_meipass(color_select_icon)
        color_select_image = load_image(color_select_icon)
        ctk.CTkButton(color_frame, text="Select color", image=color_select_image, command=self._select_color, width=1, anchor="w", compound=ctk.LEFT).grid(column=0, row=2, sticky="nw", pady=(8, 0))

        # Run button
        run_icon: Path = (Directory.RESOURCES / "menu" / "common" / "run").with_suffix(".png")
        if not run_icon.is_file():
            restore_from_meipass(run_icon)
        run_image = load_image(run_icon)
        ctk.CTkButton(container, text="Generate mod", image=run_image, command=self._run, width=1, anchor="w", compound=ctk.LEFT).grid(column=0, row=2, sticky="nsw")
        
        ctk.CTkLabel(container, textvariable=self.progress_variable, anchor="w").grid(column=0, row=3, sticky="w", pady=(4, 0))
    # endregion


    # region functions
    def _select_color(self) -> None:
        try:
            color = colorchooser.askcolor()[1]
            if not color:
                return
            self.color_variable.set(color.upper())
            self.color_visualizer.configure(fg_color=color)
        
        except Exception:
            return
    

    def _run(self) -> None:
        Thread(name="mod-generator-thread", target=self._actually_run, daemon=True).start()


    def _actually_run(self) -> None:
        name: str = self.mod_name_entry.get()
        color: str = self.color_variable.get()

        if self.is_running:
            return

        if not name:
            messagebox.showwarning(ProjectData.NAME, "Enter a name first!")
            return

        if not color or color == "None":
            messagebox.showwarning(ProjectData.NAME, "Choose a color!")
            return

        if name in [mod.name for mod in Directory.MODS.iterdir()]:
            messagebox.showerror(ProjectData.NAME, "Anther mod with the same name already exists!")
            return

        self.is_running = True
        self.root.after(0, self.progress_variable.set, "Generating, please wait")
        try:
            mod_generator.run(name, color, output_dir=Directory.MODS)
            messagebox.showinfo(ProjectData.NAME, "Mod generated successfully!")
        except Exception as e:
            messagebox.showerror(ProjectData.NAME, message=f"Error while generating mod! {type(e).__name__}: {e}")
        self.is_running = False
        self.root.after(0, self.progress_variable.set, "")
    # endregion