from pathlib import Path
import json

from modules import Logger
from modules.filesystem import File

from .create_gradient_image import create_gradient_image

from PIL import Image


def generate_imagesets(base_directory: Path, icon_map: dict[str, dict[str, dict[str, str | int]]], color1, color2, angle: int) -> None:
    icon_cache: dict[str, Image.Image] = {}
    modded_imagesets: list[str] = []
    blacklist: list[str] = get_blacklist()
    formatted_icon_map: dict[str, dict[str, Path | list[tuple[int, int, int, int]]]] = {}

    for _, icons in icon_map.items():
        for icon_name, data in icons.items():
            if icon_name in blacklist:
                continue

            image_set: str = data["image_set"]
            x: int = data["x"]
            y: int = data["y"]
            w: int = data["w"]
            h: int = data["h"]
            image_set_path: Path = (base_directory / image_set).with_suffix(".png")

            if f"{image_set}.png" not in modded_imagesets:
                modded_imagesets.append(f"{image_set}.png")

            if image_set not in formatted_icon_map:
                formatted_icon_map[image_set] = {}
                formatted_icon_map[image_set]["path"] = image_set_path
                formatted_icon_map[image_set]["icons"] = []
            
            formatted_icon_map[image_set]["icons"].append((x, y, x+w, y+h))
    
    for image_set, image_set_data in formatted_icon_map.items():
        path: Path = image_set_data["path"]
        with Image.open(path, formats=("PNG",)) as image:
            for box in image_set_data["icons"]:
                    image = image.convert("RGBA")
                    icon: Image.Image = image.crop(box)

                    r, g, b, a = icon.split()
                    modded_icon = get_mask(color1, color2, angle, icon.size, icon_cache)
                    modded_icon.putalpha(a)

                    image.paste(modded_icon, box)
            image.save(path, format="PNG", optimize=False)
    
    # Remove unmodded ImageSets
    if modded_imagesets:
        for item in base_directory.iterdir():
            if item.is_file() and item.name not in modded_imagesets:
                item.unlink()


def get_blacklist() -> list[str]:
    if not File.MOD_GENERATOR_BLACKLIST.is_file():
        Logger.warning("Icon blacklist not found!")
        return []

    try:
        with open(File.MOD_GENERATOR_BLACKLIST, "r") as file:
            data: list[str] = json.load(file)
            return data

    except Exception as e:
        Logger.error(f"Failed to get icon blacklist! {type(e).__name__}: {e}")
        return []


def get_mask(color1, color2, angle: int, size: tuple[int, int], cache: dict[str, Image.Image]) -> Image.Image:
    key: str = f"{size[0]}-{size[1]}"
    if key in cache:
        return cache[key]
    
    if color2 is None:
        mask: Image.Image = Image.new("RGBA", size, color1)
    
    else:
        mask = create_gradient_image(size, color1, color2, angle)
    
    cache[key] = mask

    return mask