import os
import tkinter as tk
import customtkinter as ctk

from modules.interface import Response
from modules.filesystem import Directory
from modules.functions.menu import error
from resources.ctk_switch_color import CTkSwitchColor
from resources.ctk_button_color import CTkButtonColor

from ..load_image import load_image

from ..fonts import *


section = None


def show(root: ctk.CTk, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int) -> None:
    destroy()
    generate(
        root=root,
        width=width,
        height=height,
        padx=padx,
        pady=pady,
        subsection_background=subsection_background
    )


def destroy() -> None:
    global section
    if section is None:
        return
    
    for widget in section.winfo_children():
        widget.destroy()


def generate(root: ctk.CTk, width: int, height: int, padx: int, pady: int, subsection_background: str|tuple[str,str]) -> None:
    global section
    section = ctk.CTkScrollableFrame(
        root,
        width=width,
        height=height,
        fg_color="transparent"
    )
    section.tkraise()
    section.grid(column=1,row=0, sticky="nsew", padx=(padx,0), pady=pady)
    section.grid_columnconfigure(0, weight=1)

    load_header(master=section, width=width)

    icon: str = os.path.join(Directory.program_files(), "resources", "icons", "common", "create.png")
    ctk.CTkButton(
        section,
        text="Create new profile",
        width=156,
        image=load_image(
            light=icon,
            dark=icon
        ),
        fg_color=CTkButtonColor.NORMAL,
        hover_color=CTkButtonColor.HOVER,
        cursor="hand2",
        command=lambda: create_new_profile(
            root=root,
            subsection_background=subsection_background,
            width=width,
            height=height,
            padx=padx,
            pady=pady
        )
    ).grid(column=0, row=1, sticky="nsw", pady=(16,24))


def load_header(master, width: int) -> None:
    header: ctk.CTkFrame = ctk.CTkFrame(
        master,
        width=width,
        fg_color="transparent"
    )
    header.grid(column=0, row=0, sticky="nsew")

    title: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text="Mods",
        anchor="w",
        justify="left",
        font=title_font
    )
    title.grid(column=0, row=0, sticky="nsew")

    description: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text="Manage your mods",
        anchor="w",
        justify="left",
        font=text_font
    )
    description.grid(column=0, row=1, sticky="nsew")