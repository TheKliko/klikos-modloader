import tkinter as tk
import customtkinter as ctk

from ..fonts import *


section = None


def show(root: ctk.CTk, background: str|tuple[str,str], width: int, height: int) -> None:
    destroy()
    generate(
        root=root,
        background=background,
        width=width,
        height=height
    )


def destroy() -> None:
    global section
    if section is None:
        return
    
    for widget in section.winfo_children():
        widget.destroy()


def generate(root: ctk.CTk, background: str|tuple[str,str], width: int, height: int) -> None:
    global section
    section = ctk.CTkScrollableFrame(
        root,
        width=width,
        height=height,
        fg_color=background
    )
    section.tkraise()
    section.grid(column=1,row=0, sticky="nsew")
    section.grid_columnconfigure(0, weight=1)

    header: ctk.CTkFrame = ctk.CTkFrame(
        section,
        width=width,
        fg_color=background
    )
    header.grid(column=0, row=0, sticky="nsew")

    title: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text="Mods",
        anchor='w',
        justify='left',
        font=title_font
    )
    title.grid(column=0, row=0, sticky="nsew")

    description: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text="Description",
        anchor='w',
        justify='left',
        font=text_font
    )
    description.grid(column=0, row=1, sticky="nsew")