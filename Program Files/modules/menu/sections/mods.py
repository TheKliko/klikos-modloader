import os
import shutil
import tkinter as tk
from tkinter.filedialog import askopenfilenames, askopenfilename
import customtkinter as ctk

from modules.interface import Response
from modules import filesystem
from modules.filesystem import Directory, extract
from modules.functions import mods
from modules.functions.menu import error
from resources.ctk_switch_color import CTkSwitchColor
from resources.ctk_button_color import CTkButtonColor

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

    button_frame = ctk.CTkFrame(
        section,
        width=width,
        fg_color="transparent"
    )
    button_frame.grid(column=0, row=1, sticky="nsew")
    button_frame.grid_columnconfigure(1, weight=1)

    package_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "mods", "package.png")
    ctk.CTkButton(
        button_frame,
        text="Add mods",
        width=108,
        image=load_image(
            light=package_icon,
            dark=package_icon
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
    ).grid(column=0, row=0, sticky="nsw", pady=(16,16))

    folder_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "mods", "folder.png")
    ctk.CTkButton(
        button_frame,
        text="Open mods folder",
        width=108,
        image=load_image(
            light=folder_icon,
            dark=folder_icon
        ),
        fg_color=CTkButtonColor.NORMAL,
        hover_color=CTkButtonColor.HOVER,
        cursor="hand2",
        anchor="w",
        compound=ctk.LEFT,
        command=lambda: filesystem.open(Directory.mods())
    ).grid(column=1, row=0, sticky="nsw", padx=8, pady=(16,16))

    load_mods(
        master=section,
        width=width,
        index=2,
        background=subsection_background,
        root=root,
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


def load_mods(master, width: int, index: int, root, background: str|tuple[str,str], height: int, padx: int, pady: int) -> None:
    def create_mod_frame(name: str, priority: int, enabled: bool, i: int) -> None:
        frame: ctk.CTkFrame = ctk.CTkFrame(
            master,
            fg_color=background
        )
        frame.grid(column=0, row=i, sticky="ew", pady=10, padx=(0,10))
        frame.grid_columnconfigure(1, weight=1)

        delete_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "common", "remove.png")
        ctk.CTkButton(
            frame,
            text="",
            image=load_image(
                light=delete_icon,
                dark=delete_icon
            ),
            width=44,
            height=44,
            fg_color=CTkButtonColor.NORMAL,
            hover_color=CTkButtonColor.HOVER,
            cursor="hand2",
            command=lambda: delete_mod(
                root=root,
                subsection_background=background,
                width=width,
                height=height,
                padx=padx,
                pady=pady,
                profile=name
            )
        ).grid(column=0, row=0, rowspan=2, padx=16)

        load_order_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )
        load_order_frame.grid(column=2, row=0, rowspan=2, padx=(16,32))

        ctk.CTkLabel(
            load_order_frame,
            text="Load order:",
            anchor="w",
            justify="left",
            font=text_font
        ).grid(column=0, row=0, sticky="nsew")

        entry = ctk.CTkEntry(
            load_order_frame,
            width=40,
            height=40,
            font=text_font
        )
        entry.grid(column=1, row=0, sticky="nsew", padx=8)
        entry.insert("end", str(priority))

        save_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "common", "save.png")
        ctk.CTkButton(
            load_order_frame,
            text="",
            image=load_image(
                light=save_icon,
                dark=save_icon,
                size=(24,24)
            ),
            width=40,
            height=40,
            fg_color=CTkButtonColor.NORMAL,
            hover_color=CTkButtonColor.HOVER,
            cursor="hand2",
            command=lambda: change_priority(
                profile=name,
                entry=entry
            )
        ).grid(column=2, row=0, sticky="nsew")

        mod_name_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )
        mod_name_frame.grid(column=1, row=0, pady=(16,0), sticky="nsew")

        ctk.CTkLabel(
            mod_name_frame,
            text=name,
            anchor="w",
            justify="left",
            font=subtitle_font
        ).grid(column=0, row=0, sticky="ew")

        rename_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "common", "rename.png")
        ctk.CTkButton(
            mod_name_frame,
            text="",
            width=40,
            height=40,
            image=load_image(
                light=rename_icon,
                dark=rename_icon,
                size=(24,24)
            ),
            fg_color=CTkButtonColor.NORMAL,
            hover_color=CTkButtonColor.HOVER,
            cursor="hand2",
            command=lambda: change_mod_name(
                old=name,
                root=root,
                subsection_background=background,
                width=width,
                height=height,
                padx=padx,
                pady=pady
            )
        ).grid(column=1, row=0, padx=8)

        # ctk.CTkLabel(
        #     frame,
        #     text="",
        #     anchor="w",
        #     justify="left",
        #     font=text_font
        # ).grid(column=1, row=1, sticky="ew", pady=(0,16))

        var = ctk.BooleanVar(value=enabled)
        var.set(enabled)

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
            command=lambda: toggle_active_state(profile=name, status=var.get())
        ).grid(column=3, row=0, rowspan=2, sticky="ew", padx=32, pady=32)

    existing_mods: list[str] = [mod for mod in os.listdir(Directory.mods()) if os.path.isdir(os.path.join(Directory.mods(), mod))]
    configured_mods: list[dict] = mods.get()
    configured_mod_names: list[str] = [data["name"] for data in configured_mods]

    for i, mod in enumerate(existing_mods, index):
        is_configured: bool = mod in configured_mod_names

        if is_configured:
            mod_data: dict = mods.get(mod)
            priority: int = mod_data["priority"]
            enabled: bool = mod_data["enabled"]

        else:
            priority = 0
            enabled = False
        
        create_mod_frame(name=mod, priority=priority, enabled=enabled, i=i)


def change_priority(profile: str, entry: ctk.CTkEntry) -> None:
    try:
        new_priority: int = int(entry.get())
    except:
        error.show("Failed to set load order!", ("Bad value: "+str(entry.get())+" (values must be an integer!)"))
        return

    data = mods.get(profile)
    if data is None and new_priority != 0:
        mods.create_profile({
            "name": profile,
            "enabled": False,
            "priority": new_priority
        })
    elif data["enabled"] == False and new_priority == 0:
        mods.delete_profile(profile)
    elif data["priority"] != new_priority:
        mods.set(name=profile, key="priority", value=new_priority)


def toggle_active_state(profile: str, status: bool) -> None:
    data = mods.get(profile)
    if data is None and status != False:
        mods.create_profile({
            "name": profile,
            "enabled": status,
            "priority": 0
        })
    elif data["priority"] == 0 and status == False:
        mods.delete_profile(profile)
    else:
        mods.set(name=profile, key="enabled", value=status)


def change_mod_name(old: str, root, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int) -> None:
    def rename_mod_folder(old: str, new: str) -> None:
        old_path: str = os.path.join(Directory.mods(), old)
        new_path: str = os.path.join(Directory.mods(), new)
        os.rename(old_path, new_path)

    try:
        dialog: ctk.CTkInputDialog = ctk.CTkInputDialog(
            text="Enter a new name",
            title="Rename Mod Profile",
            fg_color=("#f8f8f8", "#1c1c1c"),
            font=text_font,
            button_fg_color=CTkButtonColor.NORMAL,
            button_hover_color=CTkButtonColor.HOVER
        )
        response = dialog.get_input()

        if not response or str(response) == "":
            return

        rename_mod_folder(old=old, new=str(response))

    except Exception as e:
        error.show(name="Failed to rename mod!", text=type(e).__name__+": "+str(e))
        return
    
    if mods.get(old) is not None:
        mods.rename_profile(old=old, new=response)

    show(
        root=root,
        subsection_background=subsection_background,
        width=width,
        height=height,
        padx=padx,
        pady=pady
    )


def install_mod(root, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int) -> None:
    try:
        user_path: str = os.getenv("HOME") or os.getenv("USERPROFILE")
        filepaths = askopenfilenames(
            filetypes=[
                # ("Archive files", "*.zip;*.rar;*.7z"),
                ("ZIP archives", "*.zip"),
                # ("7z archives", "*.7z"),
                # ("RAR archives", "*.rar")
            ],
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


def delete_mod(root: ctk.CTk, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int, profile: str) -> None:
    dialog: ctk.CTkInputDialog = ctk.CTkInputDialog(
        text="This action cannot be undone! To continue, type \"yes\"",
        title="Delete Mod Profile",
        fg_color=("#f8f8f8", "#1c1c1c"),
        font=text_font,
        button_fg_color=CTkButtonColor.NORMAL,
        button_hover_color=CTkButtonColor.HOVER
    )
    response = str(dialog.get_input()).lower()

    if response is None or response not in Response.ACCEPT:
        return

    mods.delete_profile(name=profile)
    target: str = os.path.join(Directory.mods(), profile)
    if os.path.isdir(target):
        shutil.rmtree(target)

    show(
        root=root,
        subsection_background=subsection_background,
        width=width,
        height=height,
        padx=padx,
        pady=pady
    )


# def add_font_mod(root: ctk.CTk, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int) -> None:
#     user_path: str = os.getenv("HOME") or os.getenv("USERPROFILE")
#     filepath = askopenfilename(
#         filetypes=[("TrueType Fonts", "*.ttf")],
#         initialdir=os.path.join(user_path, "Downloads") if user_path is not None else os.path.abspath(os.sep),
#         title="Custom Font"
#     )
#     if not filepath:
#         return
    
#     mod_name: str = "Custom Font ("+os.path.basename(filepath).removesuffix(".ttf").removesuffix("-VariableFont_wght")+")"
#     mod_path: str = os.path.join(Directory.mods(), mod_name)

#     if os.path.exists(mod_path):
#         shutil.rmtree(mod_path, ignore_errors=True)
    
#     target: str = os.path.join(mod_path, "content", "fonts")
#     os.makedirs(target, exist_ok=True)
#     shutil.copy(filepath, target)

#     os.rename(os.path.join(target, os.path.basename(filepath)), os.path.join(target, "CustomFont.ttf"))
#     # generate .json file for EVERY SINGLE FONT THAT ROBLOX USES, store it in target/families

#     show(
#         root=root,
#         subsection_background=subsection_background,
#         width=width,
#         height=height,
#         padx=padx,
#         pady=pady
#     )