import os
from typing import Literal
from io import BytesIO

from modules.logger import logger
from modules import request

from customtkinter import CTkImage
from PIL import Image


_image_cache: dict[str, CTkImage] = {}


def load_image(light: str, dark: str, size: tuple[int, int]) -> CTkImage | Literal[""]:
    key: str = f"{light}-{dark}-{size}"
    cached_image = _image_cache.get(key)
    if cached_image is not None:
        return cached_image
    
    try:
        light_image = Image.open(light)
        dark_image = Image.open(dark)
        
        image: CTkImage = CTkImage(
            light_image=light_image,
            dark_image=dark_image,
            size=size
        )
        _image_cache[key] = image
        return image

    except Exception as e:
        logger.error(f"Failed to load images: {os.path.basename(light)} & {os.path.basename(dark)}, reason: {type(e).__name__}! {str(e)}")
        return ""


def load_image_from_url(url: str, size: tuple[int, int]) -> CTkImage | Literal[""]:
    key: str = f"{url}-{size}"
    cached_image = _image_cache.get(key)
    if cached_image is not None:
        return cached_image
    
    try:
        response = request.get(url, attempts=1, cache=True)
        pil_image = Image.open(BytesIO(response.content))

        image: CTkImage = CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size=size
        )
        _image_cache[key] = image
        return image

    except Exception as e:
        logger.error(f"Failed to load image from URL: \"{url}\", reason: {type(e).__name__}! {str(e)}")
        return ""