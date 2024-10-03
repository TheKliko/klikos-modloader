import os
import tkinter as tk
from tkinter import ttk
from typing import Callable, Literal

import customtkinter as ctk

from modules.filesystem.directories import Directory
from modules.info import Project

from .load_image import load_image
from .fonts import navbar_font, title_font, text_font


button_width: int = 20
button_background_active: str = ("#eaeaea", "#2d2d2d")
button_padx: int = 10
button_pady: int = 10


def create(root: ctk.CTk, background: str|tuple[str,str], buttons: list[dict[str,str|Callable]], width: int, height: int) -> ctk.CTkFrame:
    frame: ctk.CTkFrame = ctk.CTkFrame(
        root,
        fg_color=background,
        width=width,
        height=height,
        
    )
    frame.grid_propagate(False)
    frame.grid(column=0,row=0, sticky="nsew")
    frame.grid_columnconfigure(0, weight=1)

    create_header(master=frame, background=background, width=width)
    create_buttons(master=frame, background=background, buttons=buttons)

    return frame


def create_header(master, background: str|tuple[str,str], width: int) -> None:
    header = ctk.CTkFrame(
        master,
        fg_color=background,
        width=width,
        height=80
    )
    header.grid(column=0, row=0, sticky="nsew", pady=24)
    header.grid_columnconfigure(0, weight=1)
    header.grid_rowconfigure([0, 1, 2], weight=1)

    logo_path: str = os.path.join(Directory.program_files(), "resources", "icons", "logo")
    logo: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text=None,
        image=load_image(
            light=os.path.join(logo_path, "light.png"),
            dark=os.path.join(logo_path, "dark.png"),
            size=(64,64)
        ),
        anchor="center",
        justify="center"
    )
    logo.grid(column=0, row=0, sticky="nsew")
    
    title: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text=Project.NAME,
        anchor="center",
        justify="center",
        font=title_font
    )
    title.grid(column=0, row=1, sticky="nsew")
    version: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text="Version "+Project.VERSION,
        anchor="center",
        justify="center",
        font=text_font
    )
    version.grid(column=0, row=2, sticky="nsew")


def create_buttons(master, background: str|tuple[str,str], buttons) -> None:
    for i, button in enumerate(buttons):
        icon: str = button.get("icon", "") or ""
        image_path: str = os.path.join(Directory.program_files(), "resources", "icons", "navigation", icon)
        image = load_image(
            light=str(image_path)+"_light.png",
            dark=str(image_path)+"_dark.png"
        )

        create_nav_button(
            master,
            text=button.get("text", ""),
            command=button.get("command", ""),
            image=image,
            background=background
        ).grid(
            column=0,
            row=i+3,
            sticky="nsew",
            padx=button_padx,
            pady=button_pady if i == 0 else (0, button_pady)
        )


def create_nav_button(master, text: str, background: str|tuple[str,str], command: Callable | Literal[""] = "", image: ctk.CTkImage | Literal[""] = "", active_background: str|tuple[str,str] = button_background_active) -> ctk.CTkButton:
    button: ctk.CTkButton = ctk.CTkButton(
        master,
        text=text,
        command=command,
        image=image,
        width=button_width,
        compound=ctk.LEFT,
        anchor="w",
        font=navbar_font,
        fg_color=background,
        hover_color=active_background,
        text_color=("#000","#DCE4EE")
    )
    return button