from _tkinter import TclError
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional, Literal

from modules import Logger
from modules.info import ProjectData
from modules.filesystem import Directory, restore_from_meipass
from modules.functions.interface.image import load as load_image

import customtkinter as ctk


class FontImportWindow(ctk.CTkToplevel):
    BUTTON_SIZE: int = 40
    ENTRY_RATIO: float = 7.5
    root: ctk.CTk
    chosen_path: Path
    text_var: ctk.StringVar
    

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

        ctk.CTkLabel(frame, text="Chosen font:", anchor="w").grid(column=0, row=0, sticky="w")
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
        initial_dir: Path = Path().home()
        if (initial_dir / "Downloads").is_dir():
            initial_dir = initial_dir / "Downloads"

        file: str | Literal[''] = filedialog.askopenfilename(
            title=f"{ProjectData.NAME} | Import mods", initialdir=initial_dir,
            filetypes=[("TrueType Fonts", "*.ttf")]
        )

        if file == '':
            return
        
        path: Path = Path(file)
        self.text_var.set(path.with_suffix("").name)
        self.chosen_path = path


    def show(self) -> None:
        self.deiconify()
        self.geometry(self._get_geometry())
        self.focus()
        self.grab_set()
        self.wait_window()
        self._hide()


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
            raise NotImplementedError("Function not implemented!")

        except Exception as e:
            Logger.error(f"{type(e).__name__}: {e}")
            self._hide()
            messagebox.showerror(ProjectData.NAME, f"Something went wrong!\n{type(e).__name__}: {e}")