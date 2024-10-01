import logging
import os
import tkinter as tk

from customtkinter import CTkImage
from PIL import Image


loaded_images: list = []


def load_image(light: str, dark: str, size: tuple[int,int] = (24,24)) -> CTkImage:
    if not os.path.isfile(light) or not light.endswith(".png") or not os.path.isfile(dark) or not dark.endswith(".png"):
        return
    
    try:
        light_image = Image.open(light)
        dark_image = Image.open(dark)

        image = CTkImage(
            light_image=light_image,
            dark_image=dark_image,
            size=size
        )
        loaded_images.append(image)
        return image

    except Exception as e:
        logging.error("Failed to load image: "+os.path.basename(dark)+"/"+os.path.basename(light)+" - "+type(e).__name__+": "+str(e))