import os
import shutil
import tkinter as tk
from tkinter.filedialog import askopenfilenames
import customtkinter as ctk

from modules.interface import Response
from modules.filesystem import Directory, extract
from modules.functions import mods
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

    icon: str = os.path.join(Directory.program_files(), "resources", "icons", "mods", "add.png")
    ctk.CTkButton(
        section,
        text="Add mods",
        width=108,
        image=load_image(
            light=icon,
            dark=icon
        ),
        fg_color=CTkButtonColor.NORMAL,
        hover_color=CTkButtonColor.HOVER,
        cursor="hand2",
        anchor="w",
        compound=ctk.LEFT,
        command=lambda: install_mod(
            root=root,
            subsection_background=subsection_background,
            width=width,
            height=height,
            padx=padx,
            pady=pady
        )
    ).grid(column=0, row=1, sticky="nsw", pady=(16,24))

    load_mods(master=section, width=width, index=2)


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


def load_mods(master, width: int, index: int) -> None:
    pass


def change_priority(profile: str, new: int) -> None:
    if mods.get(profile) is not None:
        mods.create_profile({
            "name": profile,
            "enabled": False,
            "priority": new
        })
    mods.set(name=profile, key="priority", value=new)


def toggle_active_state(profile: str, status: bool) -> None:
    if mods.get(profile) is not None:
        mods.create_profile({
            "name": profile,
            "enabled": status,
            "priority": 0
        })
    mods.set(name=profile, key="enabled", value=status)


def change_mod_name(old: str, new: str, root, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int) -> None:
    try:
        rename_mod_folder(old=old, new=new)
    except Exception as e:
        error.show(name="Failed to rename mod!", text=type(e).__name__+": "+str(e))
        return
    
    if mods.get(old) is not None:
        mods.rename_profile(old=old, new=new)

    show(
        root=root,
        subsection_background=subsection_background,
        width=width,
        height=height,
        padx=padx,
        pady=pady
    )


def rename_mod_folder(old: str, new: str) -> None:
    old_path: str = os.path.join(Directory.mods(), old)
    new_path: str = os.path.join(Directory.mods(), new)
    os.rename(old_path, new_path)


def install_mod(root, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int) -> None:
    try:
        user_path: str = os.getenv("HOME") or os.getenv("USERPROFILE")
        filepaths = askopenfilenames(
            filetypes=[("ZIP archives", "*.zip")],
            initialdir=os.path.join(user_path, "Downloads") if user_path is not None else os.path.abspath(os.sep),
            title="Install mods"
        )
        if not filepaths:
            return
        
        for file in filepaths:
            mod_name: str = os.path.basename(file).removesuffix(".zip")
            target: str = os.path.join(Directory.mods(), mod_name)
            if os.path.isdir(target):
                dialog: ctk.CTkInputDialog = ctk.CTkInputDialog(
                    text="Mod \""+str(mod_name)+"\" already exists. To continue, type \"yes\"",
                    title="Mod installer",
                    fg_color=("#f8f8f8", "#1c1c1c"),
                    font=text_font,
                    button_fg_color=CTkButtonColor.NORMAL,
                    button_hover_color=CTkButtonColor.HOVER
                )
                response = str(dialog.get_input()).lower()

                if response is None or response not in Response.ACCEPT:
                    continue
                shutil.rmtree(target, ignore_errors=True)
            extract(
                source=file,
                destination=target
            )

        show(
            root=root,
            subsection_background=subsection_background,
            width=width,
            height=height,
            padx=padx,
            pady=pady
        )

    except Exception as e:
        error.show("Failed to install mod!", str(type(e).__name__)+": "+str(e))