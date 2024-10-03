import os
import tkinter as tk
import customtkinter as ctk
import threading
from typing import Callable

from modules.filesystem import Directory
from modules.functions import fastflags
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
    load_fastflags(
        master=section,
        background=subsection_background,
        root=root,
        width=width,
        height=height,
        padx=padx,
        pady=pady
    )


def load_header(master, width: int) -> None:
    header: ctk.CTkFrame = ctk.CTkFrame(
        master,
        width=width,
        fg_color="transparent"
    )
    header.grid(column=0, row=0, sticky="nsew")

    title: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text="FastFlags",
        anchor="w",
        justify="left",
        font=title_font
    )
    title.grid(column=0, row=0, sticky="nsew")

    description: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text="FastFlags are client settings that can be modified by the user. May cause unwanted side-effects",
        anchor="w",
        justify="left",
        font=text_font
    )
    description.grid(column=0, row=1, sticky="nsew")


def load_fastflags(master, background: str|tuple[str,str], root: ctk.CTk, width: int, height: int, padx: int, pady: int) -> None:
    all_fastflags: list = fastflags.get()

    for i, data in enumerate(all_fastflags, 1):
        create_fastflag_frame(
            master=master,
            background=background,
            profile=data,
            index=i,
            root=root,
            width=width,
            height=height,
            padx=padx,
            pady=pady
        )


def create_fastflag_frame(master, background: str|tuple[str,str], profile: dict, index: int, root: ctk.CTk, width: int, height: int, padx: int, pady: int) -> None:
    frame: ctk.CTkFrame = ctk.CTkFrame(
        master,
        fg_color=background
    )
    frame.grid(column=0, row=index, sticky="ew", pady=10, padx=(0,10))
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=0)

    name: str = profile["name"]
    description: str|None = profile.get("description", None)
    status: bool = profile["enabled"]


    configure_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "common", "configure.png")
    ctk.CTkButton(
        frame,
        text="",
        image=load_image(
            light=configure_icon,
            dark=configure_icon
        ),
        width=44,
        height=44,
        fg_color=CTkButtonColor.NORMAL,
        hover_color=CTkButtonColor.HOVER,
        cursor="hand2",
        command=lambda: configure_profile(
            root=root,
            subsection_background=background,
            width=width,
            height=height,
            padx=padx,
            pady=pady,
            data=profile
        )
    ).grid(column=0, row=0, rowspan=3, padx=16)


    ctk.CTkLabel(
        frame,
        text=name,
        anchor="w",
        justify="left",
        font=subtitle_font
    ).grid(column=1, row=0, sticky="ew", pady=(16,0) if description is not None else 16)

    if description is not None:
        ctk.CTkLabel(
            frame,
            text=description or "Description: None",
            anchor="w",
            justify="left",
            font=text_font_small,
            wraplength=500
        ).grid(column=1, row=1, sticky="ew", pady=(2,16))


    var = ctk.BooleanVar(value=status)
    var.set(status)

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
        command=lambda: toggle_fastflag_profile(name=name, value=var.get())
    ).grid(column=2, row=0, rowspan=3, sticky="ew", padx=32, pady=32)


def toggle_fastflag_profile(name: str, value: bool) -> None:
    fastflags.set(name=name, key="enabled", value=value)


def configure_profile(root: ctk.CTk, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int, data: dict) -> None:
    destroy()

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

    name: str = data["name"]
    description: str|None = data.get("description", None)
    profile_data: dict = data["data"]
    
    load_configuration_header(
        master=section,
        width=width,
        profile=name,
        profile_description=description,
        return_command = lambda: show(
            root=root,
            subsection_background=subsection_background,
            width=width,
            height=height,
            padx=padx,
            pady=pady
        )
    )
    create_fastflags_frame(master=section, width=width, data=profile_data, background=subsection_background)
    create_action_buttons(master=section, width=width, data=profile_data, background=subsection_background)


def load_configuration_header(master, width: int, profile: str, return_command: Callable, profile_description: str|None = None) -> None:
    header: ctk.CTkFrame = ctk.CTkFrame(
        master,
        width=width,
        fg_color="transparent"
    )
    header.grid(column=0, row=0, sticky="nsew")

    title: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text=str(profile),
        anchor="w",
        justify="left",
        font=title_font
    )
    title.grid(column=1, row=0, sticky="nsew")

    description: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text=str(profile_description or ""),
        anchor="w",
        justify="left",
        font=text_font
    )
    description.grid(column=1, row=1, sticky="nsew")

    return_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "common", "return.png")
    ctk.CTkButton(
        header,
        text="",
        image=load_image(
            light=return_icon,
            dark=return_icon
        ),
        width=44,
        height=44,
        fg_color=CTkButtonColor.NORMAL,
        hover_color=CTkButtonColor.HOVER,
        cursor="hand2",
        command=return_command
    ).grid(column=0, row=0, rowspan=3, padx=(0,16))


def create_fastflags_frame(master, width: int, data: dict, background: str|tuple[str,str]) -> None:
    parent = ctk.CTkFrame(
        master,
        width=width,
        fg_color="transparent"
    )
    parent.grid(column=0, row=1, sticky="nsew", pady=(16,0))
    parent.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        parent,
        text="Profile data:",
        anchor="w",
        justify="left",
        font=subtitle_font
    ).grid(column=0, row=0, sticky="ew", pady=4)

    frame = ctk.CTkScrollableFrame(
        parent,
        fg_color=background
    )
    frame.grid(column=0, row=1, sticky="ew")
    
    ctk.CTkLabel(
        frame,
        text="{",
        anchor="w",
        justify="left",
        font=code_font,
        text_color="#ce70d6"
    ).grid(column=0, row=0, sticky="ew")

    n: int = len(data)
    last: str = list(data.keys())[-1]
    for i, (k, v) in enumerate(data.items()):
        ctk.CTkLabel(
            frame,
            text="  \""+str(k)+"\": "+str(v)+("," if k != last else ""),
            anchor="w",
            justify="left",
            font=code_font,
            text_color="#7cdcfe"
        ).grid(column=0, row=i+1, sticky="ew")
    
    ctk.CTkLabel(
        frame,
        text="}",
        anchor="w",
        justify="left",
        font=code_font,
        text_color="#ce70d6"
    ).grid(column=0, row=n+1, sticky="ew")


def create_action_buttons(master, width: int, data: dict, background: str|tuple[str,str]) -> None:
    parent = ctk.CTkFrame(
        master,
        width=width,
        fg_color="transparent"
    )
    parent.grid(column=0, row=2, sticky="nsw", pady=(16,0))
    parent.grid_columnconfigure(0, weight=1)

    export_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "fastflags", "export.png")
    import_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "fastflags", "import.png")
    rename_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "common", "rename.png")
    delete_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "common", "remove.png")
    icon_size: tuple[int,int] = (16,16)

    ctk.CTkButton(
        parent,
        text="Import FastFlags",
        image=load_image(
            light=import_icon,
            dark=import_icon,
            size=icon_size
        ),
        fg_color=CTkButtonColor.NORMAL,
        hover_color=CTkButtonColor.HOVER,
        cursor="hand2",
        font=text_font,
        compound=ctk.LEFT,
        anchor="w",
        command=lambda: print("test")
    ).grid(column=0, row=0, padx=4, pady=4, sticky="ns")

    ctk.CTkButton(
        parent,
        text="Export Profile",
        image=load_image(
            light=export_icon,
            dark=export_icon,
            size=icon_size
        ),
        fg_color=CTkButtonColor.NORMAL,
        hover_color=CTkButtonColor.HOVER,
        cursor="hand2",
        font=text_font,
        compound=ctk.LEFT,
        anchor="w",
        command=lambda: print("test")
    ).grid(column=1, row=0, padx=4, pady=4, sticky="ns")
    
    ctk.CTkButton(
        parent,
        text="Rename Profile",
        image=load_image(
            light=rename_icon,
            dark=rename_icon,
            size=icon_size
        ),
        fg_color=CTkButtonColor.NORMAL,
        hover_color=CTkButtonColor.HOVER,
        cursor="hand2",
        font=text_font,
        compound=ctk.LEFT,
        anchor="w",
        command=lambda: print("test")
    ).grid(column=2, row=0, padx=4, pady=4, sticky="ns")
    
    ctk.CTkButton(
        parent,
        text="Delete Profile",
        image=load_image(
            light=delete_icon,
            dark=delete_icon,
            size=icon_size
        ),
        fg_color=CTkButtonColor.NORMAL,
        hover_color=CTkButtonColor.HOVER,
        cursor="hand2",
        font=text_font,
        compound=ctk.LEFT,
        anchor="w",
        command=lambda: print("test")
    ).grid(column=3, row=0, padx=4, pady=4, sticky="ns")