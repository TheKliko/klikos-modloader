import os

from tkinter import TclError
import customtkinter as ctk
import threading
from typing import Literal

from modules.filesystem import Directory
from modules.info import Project


class MainWindow:
    title: str = Project.NAME
    icon: str = os.path.join(Directory.program_files(), "resources", "favicon.ico")

    width: int = 520
    height: int = 320
    padding: int = 50

    size: str = str(width)+"x"+str(height)

    background: str|tuple[str,str] = ("#f8f8f8", "#1c1c1c")

    theme: str = "blue"


    def __init__(self, mode: Literal["WindowsPlayer", "WindowsStudio"]) -> None:
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme(self.theme)

        self.root: ctk.CTk = ctk.CTk()
        self.root.title(self.title)
        self.root.geometry(self.size)
        self.root.configure(fg_color=self.background, resizable=False)
        self.root.resizable(False, False)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.root.geometry(self.size+"+"+str(x)+"+"+str(y))

        icon: str = self.icon
        if os.path.isfile(icon) and icon.endswith('.ico'):
            self.root.iconbitmap(icon)
        
        from . import tasks
        
        thread = threading.Thread(
            name="launcher-thread-main",
            target=tasks.run,
            kwargs={
                "root": self.root,
                "mode": mode
            },
            daemon=True
        )
        thread.start()

        self.root.mainloop()