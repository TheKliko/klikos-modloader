import os
import tkinter as tk
import customtkinter as ctk
import threading
from typing import Any

from modules.functions import integrations
from resources.ctk_switch_color import CTkSwitchColor

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
    load_integrations(master=section, background=subsection_background)


def load_header(master, width: int) -> None:
    header: ctk.CTkFrame = ctk.CTkFrame(
        master,
        width=width,
        fg_color="transparent"
    )
    header.grid(column=0, row=0, sticky="nsew")

    title: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text="Integrations",
        anchor="w",
        justify="left",
        font=title_font
    )
    title.grid(column=0, row=0, sticky="nsew")

    description: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text="Configure integrations",
        anchor="w",
        justify="left",
        font=text_font
    )
    description.grid(column=0, row=1, sticky="nsew")


def load_integrations(master, background: str|tuple[str,str]) -> None:
    all_integrations = integrations.get()

    for i, (name, data) in enumerate(all_integrations.items(), 1):
        threading.Thread(
            target=create_integration_frame,
            args=(master,name,background,data,i)
        ).start()


def create_integration_frame(master, integration: str, background: str|tuple[str,str], data: dict[str,str], index: int) -> None:
    frame: ctk.CTkFrame = ctk.CTkFrame(
        master,
        fg_color=background
    )
    frame.grid(column=0, row=index, sticky="ew", pady=10, padx=(0,10))
    frame.grid_columnconfigure(0, weight=3)
    frame.grid_columnconfigure(1, weight=0)
    frame.grid_columnconfigure(2, weight=0)

    integration_name: str = str(data["name"])
    integration_type: str = str(data["type"]).lower()
    integration_value: Any = data["value"]
    integration_default_value: Any|None = data.get("default", None)
    
    
    ctk.CTkLabel(
        frame,
        text=integration_name,
        anchor="w",
        justify="left",
        font=subtitle_font
    ).grid(column=0, row=0, sticky="ew", padx=16, pady=(16,0))

    ctk.CTkLabel(
        frame,
        text=str(data.get("description", "Description: None")),
        anchor="w",
        justify="left",
        font=text_font,
        wraplength=500
    ).grid(column=0, row=1, sticky="ew", padx=16, pady=2 if integration_default_value is not None else (2,16))

    if integration_default_value is not None:
        ctk.CTkLabel(
            frame,
            text="Default: "+("on" if integration_type=="bool" and integration_default_value==True else "off" if integration_type=="bool" and integration_default_value==False else str(integration_default_value)),
            anchor="w",
            justify="left",
            font=text_font_small,
            wraplength=500
        ).grid(column=0, row=2, sticky="ew", padx=16, pady=(0,16))

    if integration_type in ["bool", "boolean", "toggle"]:
        var = ctk.BooleanVar(value=integration_value)
        var.set(integration_value)

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
            command=lambda: update_integration(integration=integration, var=var, value=var.get())
        ).grid(column=1, row=0, rowspan=3, sticky="ew", padx=32, pady=32)

    else:
        ctk.CTkLabel(
            frame,
            text="Value: "+str(integration_value),
            anchor="w",
            justify="left",
            font=text_font
        ).grid(column=1, row=0, rowspan=3, sticky="ew", padx=16, pady=16)


def update_integration(integration: str, var: ctk.StringVar|ctk.IntVar|ctk.BooleanVar|ctk.DoubleVar, value: Any) -> None:
    integrations.set(key=integration, value=value)
    set_var(var=var, value=value)


def set_var(var: ctk.StringVar|ctk.IntVar|ctk.BooleanVar|ctk.DoubleVar, value: Any) -> None:
    var.set(value)