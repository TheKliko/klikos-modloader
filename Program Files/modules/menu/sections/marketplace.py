import logging
import os
import subprocess
import threading

import customtkinter as ctk

from modules import request
from modules.filesystem import Directory

from ..load_image import load_image, load_image_from_url
from ..fonts import *


section = None
download_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "marketplace", "download.png")
download_button_background: str|tuple[str,str] = ("#00cc6a","#08c75e")
download_button_background_active: str|tuple[str,str] = ("#00c667","#01a851")


def show(root: ctk.CTk, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int) -> None:
    destroy()
    generate(
        root=root,
        subsection_background=subsection_background,
        width=width,
        height=height,
        padx=padx,
        pady=pady
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

    try:
        load_mods(
            master=section,
            background=subsection_background
        )
    
    except Exception as e:
        logging.warning("Marketplace failed to load!")
        logging.error(type(e).__name__+": "+str(e))
        
        show_error(
            background=subsection_background,
            exception=e,
            width=width
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
        text="Community Mods",
        anchor="w",
        justify="left",
        font=title_font
    )
    title.grid(column=0, row=0, sticky="nsew")

    description: ctk.CTkLabel = ctk.CTkLabel(
        header,
        text="Download mods with the press of a button",
        anchor="w",
        justify="left",
        font=text_font
    )
    description.grid(column=0, row=1, sticky="nsew")


def show_error(background: str|tuple[str,str], exception: Exception, width: int) -> None:
    global section
    destroy()

    load_header(master=section, width=width)

    frame: ctk.CTkFrame = ctk.CTkFrame(
        section,
        fg_color=background
    )
    frame.grid(column=0, row=1, sticky="ew", pady=10)

    ctk.CTkLabel(
        frame,
        text="Section failed to load! Please try again later . . .",
        anchor="w",
        justify="left",
        font=text_font
    ).grid(column=0, row=0, sticky="ew", padx=(8,0))

    ctk.CTkLabel(
        frame,
        text=str(type(exception).__name__)+": "+str(exception),
        anchor="w",
        justify="left",
        font=text_font
    ).grid(column=0, row=1, sticky="ew", padx=(8,0))


def load_mods(master, background: str|tuple[str,str]) -> None:
    response = request.get(request.Api.marketplace())
    mods: list[dict[str,str]] = response.json()

    for i, mod in enumerate(mods, 1):
        threading.Thread(
            target=create_mod_frame,
            args=(master,background,mod,i)
        ).start()


def create_mod_frame(master, background: str|tuple[str,str], data: dict[str,str], index: int) -> None:
    frame: ctk.CTkFrame = ctk.CTkFrame(
        master,
        fg_color=background
    )
    frame.grid(column=0, row=index, sticky="ew", pady=10, padx=(0,10))
    frame.grid_columnconfigure(0, weight=3)
    frame.grid_columnconfigure(1, weight=0)
    frame.grid_columnconfigure(2, weight=0)

    id: str = data["id"]
    name: str = data.get("name", id)
    author: str|None = data.get("author", None)
    description: str|None = data.get("description", None)
    thumbnail_url: str|None = request.Api.mod_thumbnail(id)

    ctk.CTkLabel(
        frame,
        text=str(name),
        anchor="w",
        justify="left",
        font=subtitle_font
    ).grid(column=0, row=0, sticky="ew", padx=(16,0), pady=(16,0))
    
    ctk.CTkLabel(
        frame,
        text=str(description),
        anchor="w",
        justify="left",
        font=text_font
    ).grid(column=0, row=1, sticky="ew", padx=(16,0))
    
    ctk.CTkLabel(
        frame,
        text="Made by: "+str(author or "AUTHOR_NOT_SPECIFIED"),
        anchor="w",
        justify="left",
        font=text_font_small
    ).grid(column=0, row=2, sticky="ew", padx=(16,0), pady=(0,16))

    if thumbnail_url is not None:
        try:
            image = load_image_from_url(url=thumbnail_url, size=(64,64))
            ctk.CTkLabel(
                frame,
                text="",
                image=image,
                anchor="w",
                justify="left",
                font=text_font,
                fg_color="transparent"
            ).grid(column=1, row=0, rowspan=3, sticky="ns", padx=(0, 72))
        except:
            pass
    
    ctk.CTkButton(
        frame,
        text="",
        image=load_image(
            light=download_icon,
            dark=download_icon
        ),
        width=48,
        height=48,
        fg_color=download_button_background,
        hover_color=download_button_background_active,
        cursor="hand2",
        command=lambda: download_mod(mod_id=id, mod_name=name)
    ).grid(column=2, row=0, rowspan=3, padx=(0,32))


def download_mod(mod_id: str, mod_name: str) -> None:
    filepath: str = os.path.join(Directory.program_files(), "modules", "functions", "menu", "remote_mod_download.py")
    new_command: str = "start cmd /c \"python \""+filepath+"\" \""+mod_id+"\" \""+mod_name+"\"\""
    subprocess.Popen(new_command, shell=True)