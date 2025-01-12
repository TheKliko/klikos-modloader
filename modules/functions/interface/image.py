from pathlib import Path
from typing import Literal
from io import BytesIO

from modules import Logger, request

from customtkinter import CTkImage
from PIL import Image


_image_cache: dict[str, CTkImage] = {}


def load(light: str | Path, dark: str | Path | None = None, size: tuple[int, int] = (24,24)) -> CTkImage | Literal[""]:
    light = Path(light)
    if dark is None:
        dark = light
    else:
        dark = Path(dark)

    if not light.is_file():
        raise FileNotFoundError(f"File does not exist: {light}")
    if not dark.is_file():
        raise FileNotFoundError(f"File does not exist: {dark}")

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
        Logger.error(f"Failed to load images: {light.name} & {dark.name}! {type(e).__name__}: {str(e)}")
        return ""


def load_from_url(url: str, size: tuple[int, int]) -> CTkImage | Literal[""]:
    key: str = f"{url}-{size}"
    cached_image = _image_cache.get(key)
    if cached_image is not None:
        return cached_image
    
    try:
        response = request.get(url, attempts=1, cached=True)
        pil_image = Image.open(BytesIO(response.content))

        image: CTkImage = CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size=size
        )
        _image_cache[key] = image
        return image

    except Exception as e:
        Logger.error(f"Failed to load image from URL: {url}! {type(e).__name__}: {str(e)}")
        return ""


def load_from_image(pil_image: Image.Image, identifier: str, size: tuple[int, int]) -> CTkImage | Literal[""]:
    key: str = f"{identifier}-{size}"
    cached_image = _image_cache.get(key)
    if cached_image is not None:
        return cached_image
    
    try:
        image: CTkImage = CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size=size
        )
        _image_cache[key] = image
        return image

    except Exception as e:
        Logger.error(f"Failed to load image from PIL.Image object! {type(e).__name__}: {str(e)}")
        return ""