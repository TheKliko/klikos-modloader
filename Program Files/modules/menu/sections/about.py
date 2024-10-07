import tkinter as tk
import os
import customtkinter as ctk
import logging
from typing import Callable
import functools

from modules.filesystem import Directory
from modules.functions.open_in_browser import open_in_browser
from modules.info import Project, URL, License
from resources.ctk_button_color import CTkButtonColor

from modules.functions.ctk_functions.load_image import load_image
from resources.fonts import *


section = None


def show(root: ctk.CTk, width: int, height: int, padx: int, pady: int, subsection_background: str|tuple[str,str]) -> None:
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

    load_info_frame(master=section, width=width, index=1)
    load_licenses(master=section, width=width, background=subsection_background, index=2)


def load_info_frame(master, width: int, index: int) -> None:
    def create_button(text: str, image: str, command: Callable, column: int, row: int) -> None:
        image = load_image(
            light=image,
            dark=image,
            size=icon_size
        )
        ctk.CTkButton(
            frame_bottom,
            text=str(text or ""),
            image=image,
            command=command,
            width=150,
            height=32,
            fg_color=CTkButtonColor.NORMAL,
            hover_color=CTkButtonColor.HOVER,
            cursor="hand2",
            font=text_font,
            compound=ctk.LEFT,
            anchor="w"
        ).grid(column=column, row=row, padx=4, pady=4, sticky="nsew")

    parent = ctk.CTkFrame(
        master,
        width=width,
        fg_color="transparent",
    )
    parent.grid(column=0, row=index, sticky="nsew", pady=16)
    parent.grid_columnconfigure(0, weight=1)

    frame_top = ctk.CTkFrame(
        parent,
        width=width,
        fg_color="transparent",
    )
    frame_top.grid(column=0, row=0, sticky="nsew", pady=(0,8))
    frame_top.grid_columnconfigure(1, weight=1)

    frame_bottom = ctk.CTkFrame(
        parent,
        width=width,
        height=10,
        fg_color="transparent",
    )
    frame_bottom.grid(column=0, row=1, sticky="nsew")

    github_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "about", "github.png")
    discord_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "about", "discord.png")
    icon_size: tuple[int,int] = (16,16)

    buttons: list[dict] = [
        {
            "text": "View on GitHub",
            "image": github_icon,
            "command": lambda: open_in_browser(
                url=URL.GITHUB
            )
        },
        {
            "text": "Join our Discord",
            "image": discord_icon,
            "command": lambda: open_in_browser(
                url=URL.DISCORD
            )
        }
    ]
    for i, data in enumerate(buttons):
        button_per_row: int = 5
        column: int = i % button_per_row
        row: int = i // button_per_row
        create_button(
            text=data["text"],
            image=data["image"],
            command=data["command"],
            column=column,
            row=row
        )


    image: str = os.path.join(Directory.program_files(), "resources", "icons", "about", "logo.png")
    ctk.CTkLabel(
        frame_top,
        text="",
        anchor="w",
        justify="left",
        image=load_image(
            light=image,
            dark=image,
            size=(64,64)
        )
    ).grid(column=0, row=0, rowspan=3, sticky="nsew", padx=(0,16))

    ctk.CTkLabel(
        frame_top,
        text=str(Project.NAME),
        anchor="w",
        justify="left",
        font=title_font
    ).grid(column=1, row=0, sticky="nsew")
    ctk.CTkLabel(
        frame_top,
        text="Made by "+str(Project.AUTHOR),
        anchor="w",
        justify="left",
        font=text_font
    ).grid(column=1, row=1, sticky="nsew")

    ctk.CTkLabel(
        frame_top,
        text="Version "+str(Project.VERSION),
        anchor="w",
        justify="left",
        font=text_font_small
    ).grid(column=1, row=2, sticky="nsew")


def load_licenses(master, width: int, background: str|tuple[str,str], index: int) -> None:
    parent = ctk.CTkFrame(
        master,
        width=width,
        fg_color="transparent",
    )
    parent.grid(column=0, row=index, sticky="nsew", pady=16)
    parent.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        parent,
        text="Licenses",
        anchor="w",
        justify="left",
        font=subtitle_font
    ).grid(column=0, row=0, sticky="nsew")

    box_width: int = 225
    box_padding: int = 8
    frame: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(
        parent,
        width=width,
        height=108,
        fg_color="transparent",
        orientation="horizontal"
    )
    frame.grid(column=0, row=1, sticky="nsew")

    licenses: list[dict[str, str | list[str]]] = License.all()
    n: int = len(licenses)-1
    for i, item in enumerate(licenses):
        try:
            name: str = str(item["name"])
            owner: str = str(item["owner"])
            license_type: str = str(item["type"])
            url = item.get("url", None)

            license_box = ctk.CTkFrame(
                frame,
                width=box_width,
                fg_color=background
            )
            license_box.grid(column=i, row=0, sticky="nsew", padx=(0,8) if i != n else 0)
            license_box.grid_rowconfigure(2, weight=1)

            ctk.CTkLabel(
                license_box,
                text=name,
                anchor="w",
                justify="left",
                font=text_font
            ).grid(column=0, row=0, sticky="nsew", padx=(box_padding, 0), pady=(box_padding,0))

            ctk.CTkLabel(
                license_box,
                text="by "+owner,
                anchor="w",
                justify="left",
                font=text_font_small
            ).grid(column=0, row=1, sticky="nsew", padx=(box_padding, 0))

            ctk.CTkLabel(
                license_box,
                text="Type: "+license_type,
                anchor="w",
                justify="left",
                font=text_font_small
            ).grid(column=0, row=2, sticky="nsew", padx=(box_padding, 0), pady=(0, box_padding))

            open_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "about", "external.png")
            ctk.CTkButton(
                license_box,
                text="",
                width=36,
                height=36,
                command=functools.partial(open_in_browser, url=url),
                image=load_image(
                    light=open_icon,
                    dark=open_icon,
                    size=(24,24)
                ),
                fg_color=CTkButtonColor.NORMAL,
                hover_color=CTkButtonColor.HOVER,
                cursor="hand2",
                font=text_font_small
            ).grid(column=1, row=0, rowspan=3, sticky="nsew", padx=(2*box_padding, box_padding), pady=box_padding)

        except Exception as e:
            logging.warning("error while loading license!")
            logging.error(type(e).__name__+": "+str(e))
            continue