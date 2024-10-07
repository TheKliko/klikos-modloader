import os
import customtkinter as ctk

from resources.fonts import *
from modules.functions.ctk_functions.load_image import load_image
from modules.filesystem import Directory


root: ctk.CTk = None
frame: ctk.CTkFrame = None
phase_label: ctk.CTkLabel = None
description_label: ctk.CTkLabel = None
image_label: ctk.CTkLabel = None

launcher_image: str = os.path.join(Directory.program_files(), "resources", "launcher.png")
image_size: tuple[int,int] = (144,144)
image = load_image(
    light=launcher_image,
    dark=launcher_image,
    size=image_size
)

phase_name: str
current_phase: int = 0
max_phase: int = 0



def set_launcher_stage(set_phase_name: str|None = None, set_current_phase: int|None = None, set_max_phase: int|None = None, set_root: ctk.CTk|None = None) -> None:
    global phase_name, current_phase, max_phase, root, phase_label, description_label, image_label, image, frame

    if set_phase_name:
        phase_name = set_phase_name
    if set_current_phase:
        current_phase = set_current_phase
    if set_max_phase:
        max_phase = set_max_phase
    
    if set_root:
        root = set_root

    if not root:
        raise Exception("No root window!")

    if set_root:
        if root:
            for widget in root.winfo_children():
                widget.destroy()
        root = set_root

        frame = ctk.CTkFrame(
            root,
            fg_color="transparent"
        )
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.grid_columnconfigure(1, weight=1)

        image_label = ctk.CTkLabel(
            frame,
            text="",
            image=image
        )
        image_label.grid(column=0, row=0, sticky="nsew")

        phase_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )
        phase_frame.grid(column=0, row=1, sticky="nsew", pady=(24,16))
        phase_frame.grid_columnconfigure(0, weight=1)
        phase_frame.grid_columnconfigure(1, weight=1)

        phase_label = ctk.CTkLabel(
            phase_frame,
            text="["+str(current_phase)+"/"+str(max_phase)+"]",
            anchor="w",
            justify="left",
            font=subtitle_font
        )
        phase_label.grid(column=0, row=0, sticky="e")

        description_label = ctk.CTkLabel(
            phase_frame,
            text=str(phase_name),
            anchor="w",
            justify="left",
            font=subtitle_font
        )
        description_label.grid(column=1, row=0, sticky="w", padx=(8,0))

        progress_bar = ctk.CTkProgressBar(
            frame,
            mode="indetermintate",
            width=256,
            fg_color=("#e6e6e6", "#2a2a2a"),
            progress_color="#cc0037"
        )
        progress_bar.grid(column=0, row=2, sticky="ns")
        progress_bar.start()
    
    else:
        if set_current_phase or set_max_phase:
            phase_label.configure(text="["+str(current_phase)+"/"+str(max_phase)+"]")
        if set_phase_name:
            description_label.configure(text=str(phase_name))