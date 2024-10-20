import os
import sys

from modules.info import ProjectData
from modules.filesystem import Directory

IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    import customtkinter as ctk
else:
    try:
        import customtkinter as ctk
    except ImportError:
        sys.path.insert(0, os.path.join(Directory.root(), "libraries"))
        import customtkinter as ctk


icon_path_extension: str = os.path.join("resources", "favicon.ico")
icon_path: str | None = os.path.join(Directory.root(), icon_path_extension)
if not os.path.isfile(icon_path):
    if IS_FROZEN:
        icon_path = os.path.join(Directory._MEI(), icon_path_extension)
    else:
        icon_path = None

theme_path_extension: str = os.path.join("resources", "theme.json")
theme_path: str = os.path.join(Directory.root(), theme_path_extension)
if not os.path.isfile(theme_path):
    if IS_FROZEN:
        theme_path = os.path.join(Directory._MEI(), theme_path_extension)
    else:
        theme_path = "blue"


class MainWindow:
    root: ctk.CTk

    width: int = 1100
    height: int = 600
    size: str = f"{width}x{height}"

    navigation_width: int = 250

    title: str = "Modloader Menu"
    icon: str = icon_path
    theme: str = theme_path
    appearance: str = "System"

    def __init__(self) -> None:
        ctk.set_appearance_mode(self.appearance)
        ctk.set_default_color_theme(self.theme)

        self.root = ctk.CTk()
        self.root.title(self.title)
        self.root.geometry(self.size)
        self.root.minsize(self.width, self.height)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.root.geometry(f"{self.size}+{x}+{y}")

        if self.icon is not None:
            self.root.iconbitmap(self.icon)
        
        ctk.CTkLabel(
            self.root,
            text="Modloader menu!",
            font=ctk.CTkFont(weight="bold", size=16)
        ).pack(expand=True, fill=ctk.BOTH)
    

    def show(self) -> None:
        self.root.mainloop()