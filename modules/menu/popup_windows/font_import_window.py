from _tkinter import TclError
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional, Literal, Callable
from tempfile import TemporaryDirectory
import json
import shutil

from modules import Logger
from modules.info import ProjectData
from modules.filesystem import Directory, restore_from_meipass, download, extract
from modules.request import Api
from modules.functions.interface.image import load as load_image
from modules.launcher.deployment_info import Deployment

import customtkinter as ctk
from fontTools.ttLib import TTFont


class FontImportWindow(ctk.CTkToplevel):
    BUTTON_SIZE: int = 40
    ENTRY_RATIO: float = 7.5
    root: ctk.CTk
    chosen_path: Optional[Path] = None
    text_var: ctk.StringVar
    on_success: Callable | None = None
    

    def __init__(self, root: ctk.CTk, *args, **kwargs) -> None:
        self.text_var = ctk.StringVar(value="Select a file")
        self.root = root
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._hide)
        self.bind("<Escape>", self._hide)

        # Hide window immediately after it's created. Only show it when needed
        self.withdraw()

        if not self.root.Constants.FAVICON.is_file():
            restore_from_meipass(self.root.Constants.FAVICON)
        self.iconbitmap(self.root.Constants.FAVICON.resolve())
        self.after(200, lambda: self.iconbitmap(self.root.Constants.FAVICON.resolve()))
        self.title(f"{ProjectData.NAME} | Font selector")

        frame: ctk.CTkFrame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(column=0, row=0, sticky="nsew", padx=32, pady=32)

        ctk.CTkLabel(frame, text="Choose a font:", anchor="w").grid(column=0, row=0, sticky="w")
        entry: ctk.CTkEntry = ctk.CTkEntry(frame, textvariable=self.text_var, state="disabled", width=int(self.ENTRY_RATIO * self.BUTTON_SIZE), height=self.BUTTON_SIZE)
        entry.grid(column=0, row=1, sticky="w")

        file_select_icon: Path = (Directory.RESOURCES / "menu" / "common" / "file-select").with_suffix(".png")
        if not file_select_icon.is_file():
            restore_from_meipass(file_select_icon)
        file_select_image = load_image(file_select_icon)
        
        run_icon: Path = (Directory.RESOURCES / "menu" / "common" / "run").with_suffix(".png")
        if not run_icon.is_file():
            restore_from_meipass(run_icon)
        run_image = load_image(run_icon)

        ctk.CTkButton(frame, image=file_select_image, command=self._select_file, text="", width=self.BUTTON_SIZE, height=self.BUTTON_SIZE).grid(column=1, row=1, sticky="w", padx=(4,8))
        ctk.CTkButton(frame, image=run_image, command=self._create_font_mod, text="", width=self.BUTTON_SIZE, height=self.BUTTON_SIZE).grid(column=2, row=1, sticky="w")

        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        self.geometry(self._get_geometry(width, height))
    

    def _select_file(self) -> None:
        initial_dir: Path = Path.home()
        if (initial_dir / "Downloads").is_dir():
            initial_dir = initial_dir / "Downloads"

        file: str | Literal[''] = filedialog.askopenfilename(
            title=f"{ProjectData.NAME} | Import mods", initialdir=initial_dir,
            filetypes=[("Supported Fonts", "*.ttf;*.otf"), ("TrueType Fonts", "*.ttf"), ("OpenType Fonts", "*.otf")]
        )

        if file == '':
            return
        
        path: Path = Path(file)
        self.text_var.set(path.with_suffix("").name)
        self.chosen_path = path
    

    def set_refresh_function(self, func: Callable) -> None:
        self.on_success = func


    def show(self) -> None:
        self.deiconify()
        self.geometry(self._get_geometry())
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
    

    def _create_font_mod(self) -> None:
        try:
            if self.chosen_path is None:
                return
                
            if not self.chosen_path.is_file():
                messagebox.showerror(ProjectData.NAME, f"File not found: {self.chosen_path.name}")
                return
            mod_name: str = f"Custom Font ({self.chosen_path.with_suffix('').name})"
            target_path: Path = Directory.MODS / mod_name

            if target_path.is_dir():
                if not messagebox.askokcancel(ProjectData.NAME, "Another mod with the same name already exists!\nDo you wish to replace it?"):
                    return
                shutil.rmtree(target_path)
            
            with TemporaryDirectory() as tmp:
                temporary_directory: Path = Path(tmp)
                fonts_basepath: Path = temporary_directory / mod_name / "content" / "fonts"
                font_filepath: Path = fonts_basepath / "CustomFont.ttf"
                font_families_path: Path = fonts_basepath / "families"
                font_families_path.mkdir(parents=True, exist_ok=True)

                # Move fonts to temporary folder, convert to .ttf if needed
                match self.chosen_path.suffix:
                    case ".ttf":
                        pass

                    case ".otf":
                        TTFont(self.chosen_path).save(font_filepath)

                    case _:
                        raise Exception("Unsupported filetype!")
            
                deployment: Deployment = Deployment("Player")
                download(Api.Roblox.Deployment.download(deployment.version, "content-fonts.zip"), temporary_directory / "content-fonts.zip")
                extract(temporary_directory / "content-fonts.zip", temporary_directory / "content-fonts-extracted")
                shutil.copytree(temporary_directory / "content-fonts-extracted" / "families", font_families_path, dirs_exist_ok=True)
                
                # Overwrite each font's json file to direct to our custom font
                new_rbxasset: str = "rbxasset://fonts//CustomFont.ttf"
                json_files: list[Path] = [
                    font_families_path / file for file in font_families_path.iterdir()
                    if file.is_file() and file.suffix == "json"
                ]
                for json_file in json_files:
                    with open(json_file, "r") as read_file:
                        data: dict = json.load(read_file)

                    faces: Optional[list[dict]] = data.get("faces")
                    if faces is None:
                        continue

                    for i, _ in enumerate(faces):
                        faces[i]["assetId"] = new_rbxasset
                    data["faces"] = faces

                    with open(json_file, "w") as write_file:
                        json.dump(data, write_file, indent=4)
                
                shutil.copytree(temporary_directory / mod_name, target_path, dirs_exist_ok=True)
            self._hide()
            if self.on_success is not None:
                self.on_success()

        except Exception as e:
            Logger.error(f"{type(e).__name__}: {e}")
            self._hide()
            messagebox.showerror(ProjectData.NAME, f"Something went wrong!\n{type(e).__name__}: {e}")