import os
import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import customtkinter as ctk
import json
from typing import Callable

from modules.interface import Response
from modules.filesystem import Directory
from modules.functions import fastflags
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

    load_fastflags(
        master=section,
        background=subsection_background,
        root=root,
        width=width,
        height=height,
        padx=padx,
        pady=pady,
        row=2
    )


def load_header(master, width: int) -> None:
    header: ctk.CTkFrame = ctk.CTkFrame(
        master,
        width=width,
        fg_color="transparent"
    )
    header.grid(column=0, row=0, sticky="nsew")
    header.grid_columnconfigure(0, weight=1)

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
    description.grid(column=0, row=1, columnspan=2, sticky="nsew")


def load_fastflags(master, background: str|tuple[str,str], root: ctk.CTk, width: int, height: int, padx: int, pady: int, row: int) -> None:
    all_fastflags: list = fastflags.get()
  
    for i, data in enumerate(all_fastflags, row):
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
    fastflags_frame = create_fastflags_frame(master=section, width=width, data=profile_data, full_data=data, background=subsection_background)
    create_action_buttons(
        master=section,
        root=root,
        width=width,
        height=height,
        padx=padx,
        pady=pady,
        full_data=data,
        background=subsection_background,
        fastflags_frame=fastflags_frame
    )


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


def create_fastflags_frame(master, width: int, data: dict, full_data: dict, background: str|tuple[str,str]) -> ctk.CTkTextbox:
    parent = ctk.CTkFrame(
        master,
        width=width,
        fg_color="transparent"
    )
    parent.grid(column=0, row=1, sticky="nsew", pady=(16,0))
    parent.grid_columnconfigure(1, weight=1)

    frame = ctk.CTkTextbox(
        parent,
        fg_color=background,
        font=code_font,
        wrap="none",
        text_color="#9cdcfe"
    )
    frame.delete(0.0, "end")
    frame.insert("end", json.dumps(data, indent=4))
    frame.grid(column=0, row=1, columnspan=2, sticky="ew")

    ctk.CTkLabel(
        parent,
        text="Profile data:",
        anchor="w",
        justify="left",
        font=subtitle_font
    ).grid(column=1, row=0, sticky="nsew", pady=4)

    save_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "common", "save.png")
    icon_size: tuple[int,int] = (16,16)
    image = load_image(
        light=save_icon,
        dark=save_icon,
        size=icon_size
    )
    button_padding: int = 8
    ctk.CTkButton(
        parent,
        text="Save",
        image=image,
        command=lambda: update_fastflags(data=full_data, textbox_frame=frame),
        width=70,
        height=32,
        fg_color=CTkButtonColor.NORMAL,
        hover_color=CTkButtonColor.HOVER,
        cursor="hand2",
        font=text_font,
        compound=ctk.LEFT,
        anchor="w"
    ).grid(column=0, row=0, padx=(0,button_padding), pady=(0,button_padding), sticky="nsew")

    return frame


def create_action_buttons(master, root, width: int, height: int, padx: int, pady: int, full_data: dict, background: str|tuple[str,str], fastflags_frame) -> None:
    def create_button(text: str, image: str, command: Callable, column: int, row: int) -> None:
        image = load_image(
            light=image,
            dark=image,
            size=icon_size
        )
        ctk.CTkButton(
            parent,
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
        fg_color="transparent"
    )
    parent.grid(column=0, row=2, sticky="nsw", pady=(16,0))
    parent.grid_columnconfigure(0, weight=1)

    export_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "fastflags", "export.png")
    import_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "fastflags", "import.png")
    rename_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "common", "rename.png")
    delete_icon: str = os.path.join(Directory.program_files(), "resources", "icons", "common", "remove.png")
    icon_size: tuple[int,int] = (16,16)

    buttons: list[dict] = [
        {
            "text": "Import FastFlags",
            "image": import_icon,
            "command": lambda: import_fastflags(
                profile_data=full_data,
                fastflag_frame=fastflags_frame
            )
        },
        {
            "text": "Export FastFlags",
            "image": export_icon,
            "command": lambda: export_fastflags(
                fastflag_frame=fastflags_frame
            )
        },
        {
            "text": "Delete Profile",
            "image": delete_icon,
            "command": lambda: delete_profile(
                root=root,
                subsection_background=background,
                width=width,
                height=height,
                padx=padx,
                pady=pady,
                data=full_data
            )
        },
        {
            "text": "Rename profile",
            "image": rename_icon,
            "command": lambda: rename_profile(
                root=root,
                subsection_background=background,
                width=width,
                height=height,
                padx=padx,
                pady=pady,
                data=full_data
            )
        },
        {
            "text": "Change description",
            "image": rename_icon,
            "command": lambda: change_profile_description(
                root=root,
                subsection_background=background,
                width=width,
                height=height,
                padx=padx,
                pady=pady,
                data=full_data
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


def update_fastflags(data: dict, textbox_frame: ctk.CTkTextbox) -> None:
    try:
        new_data_string = textbox_frame.get("0.0", "end")
        new_data: dict = json.loads(new_data_string)
        if new_data == new_data_string:
            return
        fastflags.set(data["name"], "data", new_data)

    except Exception as e:
        error.show("Failed to save FastFlag profile", str(type(e).__name__)+": "+str(e))


def rename_profile(root: ctk.CTk, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int, data: dict) -> None:
    old_name = data["name"]

    dialog: ctk.CTkInputDialog = ctk.CTkInputDialog(
        text="Choose a new name!",
        title="Rename FastFlag Profile",
        fg_color=("#f8f8f8", "#1c1c1c"),
        font=text_font,
        button_fg_color=CTkButtonColor.NORMAL,
        button_hover_color=CTkButtonColor.HOVER
    )
    new_name = dialog.get_input()

    if new_name is None:
        return

    data["name"] = new_name
    
    fastflags.rename_profile(old=old_name, new=new_name)
    configure_profile(
        root=root,
        subsection_background=subsection_background,
        width=width,
        height=height,
        padx=padx,
        pady=pady,
        data=data
    )


def change_profile_description(root: ctk.CTk, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int, data: dict) -> None:
    old_description = data["description"]

    dialog: ctk.CTkInputDialog = ctk.CTkInputDialog(
        text="Choose a new description!",
        title="FastFlag profile description",
        fg_color=("#f8f8f8", "#1c1c1c"),
        font=text_font,
        button_fg_color=CTkButtonColor.NORMAL,
        button_hover_color=CTkButtonColor.HOVER
    )
    new_description = dialog.get_input()

    if new_description is None:
        return

    data["description"] = new_description
    
    fastflags.change_profile_description(old=old_description, new=new_description)
    configure_profile(
        root=root,
        subsection_background=subsection_background,
        width=width,
        height=height,
        padx=padx,
        pady=pady,
        data=data
    )


def delete_profile(root: ctk.CTk, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int, data: dict) -> None:
    profile_name = data["name"]

    dialog: ctk.CTkInputDialog = ctk.CTkInputDialog(
        text="This action cannot be undone! To continue, type \"yes\"",
        title="Delete FastFlag Profile",
        fg_color=("#f8f8f8", "#1c1c1c"),
        font=text_font,
        button_fg_color=CTkButtonColor.NORMAL,
        button_hover_color=CTkButtonColor.HOVER
    )
    response = str(dialog.get_input()).lower()

    if response is None or response not in Response.ACCEPT:
        return
    
    fastflags.delete_profile(name=profile_name)
    show(
        root=root,
        subsection_background=subsection_background,
        width=width,
        height=height,
        padx=padx,
        pady=pady
    )


def import_fastflags(profile_data: dict, fastflag_frame):
    try:
        user_path: str = os.getenv("HOME") or os.getenv("USERPROFILE")
        filepath: str = askopenfilename(
            filetypes=[("JSON files", "*.json")],
            initialdir=os.path.join(user_path, "Downloads") if user_path is not None else os.path.abspath(os.sep),
            defaultextension=".json",
            title="Export FastFlags"
        )
        if not filepath:
            return
        with open(filepath, "r") as file:
            data = json.load(file)
        profile_data["data"].update(data)
        data_string = json.dumps(profile_data["data"], indent=4)
        fastflag_frame.delete(0.0, "end")
        fastflag_frame.insert(0.0, data_string)

        update_fastflags(data=profile_data, textbox_frame=fastflag_frame)

    except Exception as e:
        error.show("Failed to export FastFlag profile", str(type(e).__name__)+": "+str(e))


def export_fastflags(fastflag_frame):
    try:
        user_path: str = os.getenv("HOME") or os.getenv("USERPROFILE")
        data_string: str = str(fastflag_frame.get(0.0, "end"))
        data: dict = json.loads(data_string)

        filepath: str = asksaveasfilename(
            filetypes=[("JSON files", "*.json")],
            initialdir=os.path.join(user_path, "Downloads") if user_path is not None else os.path.abspath(os.sep),
            initialfile="ClientAppSettings.json",
            defaultextension=".json",
            title="Export FastFlags"
        )
        if not filepath:
            return
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        error.show("Failed to export FastFlag profile", str(type(e).__name__)+": "+str(e))


def create_new_profile(root, subsection_background: str|tuple[str,str], width: int, height: int, padx: int, pady: int) -> None:
    profile_data: dict = {
        "name": None,
        "description": None,
        "enabled": True,
        "data": {
            "exampleFlag": "exampleValue"
        }
    }

    dialog: ctk.CTkInputDialog = ctk.CTkInputDialog(
        text="Choose a name for your profile",
        title="Create FastFlag Profile",
        fg_color=("#f8f8f8", "#1c1c1c"),
        font=text_font,
        button_fg_color=CTkButtonColor.NORMAL,
        button_hover_color=CTkButtonColor.HOVER
    )

    name = dialog.get_input()

    if name is None or name == "":
        return
    name = str(name)
    
    if fastflags.get(name) is not None:
        error.show("Failed to create FastFlag profile", "A profile with the same name already exists")
    
    profile_data["name"] = name
    fastflags.create_profile(profile_data=profile_data)

    configure_profile(
        root=root,
        subsection_background=subsection_background,
        width=width,
        height=height,
        padx=padx,
        pady=pady,
        data=profile_data
    )