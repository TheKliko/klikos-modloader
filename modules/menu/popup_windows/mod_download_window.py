from _tkinter import TclError
from typing import Optional

from modules.info import ProjectData
from modules.filesystem import restore_from_meipass
from modules.functions.interface.image import load as load_image

import customtkinter as ctk


class ModDownloadWindow(ctk.CTkToplevel):
    root: ctk.CTk
    textvariable: ctk.StringVar


    def __init__(self, root: ctk.CTk, *args, **kwargs) -> None:
        self.textvariable = ctk.StringVar(value="placeholder")
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
        self.title(f"{ProjectData.NAME} | Mod downloader")

        frame: ctk.CTkFrame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(column=0, row=0, sticky="nsew", padx=32, pady=32)

        ctk.CTkLabel(frame, textvariable=self.textvariable).grid(column=0, row=0)

        progress_bar: ctk.CTkProgressBar = ctk.CTkProgressBar(self, mode="indeterminate", corner_radius=0, width=460, height=20)
        progress_bar.grid(column=0, row=1)
        progress_bar.start()

        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        self.geometry(self._get_geometry(width, height))


    def show(self, name: str) -> ctk.StringVar:
        self.textvariable.set(f"Downloading {name}")
        self.deiconify()
        self.geometry(self._get_geometry())
        self.grab_set()
        self.wm_transient(self.root)
        return self.textvariable


    def _get_geometry(self, width: Optional[int] = None, height: Optional[int] = None) -> str:
        root_geometry: str = self.root.winfo_geometry()
        root_size, root_x, root_y = root_geometry.split("+")
        root_width, root_height = map(int, root_size.split("x"))

        self.update_idletasks()
        # width = width or self.winfo_width()
        # height = height or self.winfo_height()
        width = width or self.winfo_reqwidth()
        height = height or self.winfo_reqheight()

        x: int = int(root_x) + ((root_width - width) // 2)
        y: int = int(root_y) + ((root_height - height) // 2)

        return f"{width}x{height}+{x}+{y}"
    

    def _hide(self, *args, **kwargs) -> None:
        try:
            self.grab_release()
            self.withdraw()
        except TclError:
            pass
    

    def hide(self, *args, **kwargs) -> None:
        self._hide()
        self.textvariable.set("placeholder")