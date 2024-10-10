import os
import tkinter as tk
import customtkinter as ctk
import threading
from typing import Any

from modules.functions import settings
from resources.ctk_switch_color import CTkSwitchColor

from modules.functions.ctk_functions.load_image import load_image
from resources.fonts import *


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


def generate(root: ctk.CTk, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int) -> None:
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
    load_settings(master=section, background=subsection_background)


def load_header(master, width: int) -> None:
    header: ctk.CTkFrame = ctk.CTkFrame(
        master,
        width=width,
        fg_color="transparent"
    )
    header.grid(column=0, row=0, sticky="nsew")

    title: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text="Settings",
        anchor="w",
        justify="left",
        font=title_font
    )
    title.grid(column=0, row=0, sticky="nsew")

    description: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text="Configure settings",
        anchor="w",
        justify="left",
        font=text_font
    )
    description.grid(column=0, row=1, sticky="nsew")


def load_settings(master, background: str|tuple[str,str]) -> None:
    all_settings = settings.get()

    for i, (name, data) in enumerate(all_settings.items(), 1):
        threading.Thread(
            target=create_setting_frame,
            args=(master,name,background,data,i)
        ).start()


def create_setting_frame(master, setting: str, background: str|tuple[str,str], data: dict[str,str], index: int) -> None:
    frame: ctk.CTkFrame = ctk.CTkFrame(
        master,
        fg_color=background
    )
    frame.grid(column=0, row=index, sticky="ew", pady=10, padx=(0,10))
    frame.grid_columnconfigure(0, weight=3)
    frame.grid_columnconfigure(1, weight=0)
    frame.grid_columnconfigure(2, weight=0)

    setting_name: str = str(data["name"])
    setting_type: str = str(data["type"]).lower()
    setting_value: Any = data["value"]
    setting_default_value: Any|None = data.get("default", None)
    
    
    ctk.CTkLabel(
        frame,
        text=setting_name,
        anchor="w",
        justify="left",
        font=subtitle_font
    ).grid(column=0, row=0, sticky="ew", padx=16, pady=(16,0))

    # description_box = ctk.CTkTextbox(
    #     frame,
    #     fg_color=background,
    #     height=60,
    #     font=text_font,
    #     wrap="word"
    # )
    # description_box.insert("end", str(data.get("description", "Description: None")))
    # description_box.configure(state="disabled")
    # description_box.grid(column=0, row=1, sticky="ew", padx=8, pady=2 if setting_default_value is not None else (2,16))

    ctk.CTkLabel(
        frame,
        text=str(data.get("description", "Description: None")),
        anchor="w",
        justify="left",
        font=text_font,
        wraplength=700
    ).grid(column=0, row=1, sticky="ew", padx=16, pady=2 if setting_default_value is not None else (2,16))

    if setting_default_value is not None:
        ctk.CTkLabel(
            frame,
            text="Default: "+("on" if setting_type=="bool" and setting_default_value==True else "off" if setting_type=="bool" and setting_default_value==False else str(setting_default_value)),
            anchor="w",
            justify="left",
            font=text_font_small,
            wraplength=500
        ).grid(column=0, row=2, sticky="ew", padx=16, pady=(0,16))

    if setting_type in ["bool", "boolean", "toggle"]:
        var = ctk.BooleanVar(value=setting_value)
        var.set(setting_value)

        ctk.CTkSwitch(
            frame,
            width=48,
            height=24,
            fg_color=CTkSwitchColor.OFF,
            progress_color=CTkSwitchColor.ON,
            text="",
            cursor="hand2",
            variable=var,
            onvalue=True,
            offvalue=False,
            command=lambda: update_setting(setting=setting, var=var, value=var.get())
        ).grid(column=1, row=0, rowspan=3, sticky="ew", padx=16, pady=16)

    else:
        ctk.CTkLabel(
            frame,
            text="Value: "+str(setting_value),
            anchor="w",
            justify="left",
            font=text_font
        ).grid(column=1, row=0, rowspan=3, sticky="ew", padx=16, pady=16)


def update_setting(setting: str, var: ctk.StringVar|ctk.IntVar|ctk.BooleanVar|ctk.DoubleVar, value: Any) -> None:
    settings.set(key=setting, value=value)
    set_var(var=var, value=value)


def set_var(var: ctk.StringVar|ctk.IntVar|ctk.BooleanVar|ctk.DoubleVar, value: Any) -> None:
    var.set(value)