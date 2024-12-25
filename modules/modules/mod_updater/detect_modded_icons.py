from pathlib import Path

from .exceptions import ImageSetsNotFoundError

from PIL import Image


def detect_modded_icons(modded_imagesets: Path, unmodded_imagesets: Path, icon_map: dict[str, dict[str, dict[str, str | int]]]) -> dict[str, list[str]]:
    modded_icons: dict[str, list[str]] = {}
    
    for size, icons in icon_map.items():
        for icon, data in icons.items():
            image_set: str = data["image_set"]
            x: int = data["x"]
            y: int = data["y"]
            w: int = data["w"]
            h: int = data["h"]

            modded_image_set_path: Path = (modded_imagesets / image_set).with_suffix(".png")
            unmodded_image_set_path: Path = (unmodded_imagesets / image_set).with_suffix(".png")

            if not modded_image_set_path.is_file():
                continue

            if not unmodded_image_set_path.is_file():
                raise ImageSetsNotFoundError(f"Failed to find unmodded ImageSet: {image_set}.png")
            
            with Image.open(modded_image_set_path, formats=("PNG",)) as file:
                modded_icon: Image.Image = file.convert("RGBA").crop((x, y, x+w, y+h))

            with Image.open(unmodded_image_set_path, formats=("PNG",)) as file:
                unmodded_icon: Image.Image = file.convert("RGBA").crop((x, y, x+w, y+h))
            
            if not is_modded_image(modded_icon, unmodded_icon):
                continue

            if size not in modded_icons:
                modded_icons[size] = []
            modded_icons[size].append(icon)
            
            # preview: Image.Image = Image.new(mode="RGBA", size=(w*2, h))
            # preview.paste(unmodded_icon, (0,0))
            # preview.paste(modded_icon, (w,0))
            # print(icon)
            # image_preview(preview)
    return modded_icons


def is_modded_image(image1: Image.Image, image2: Image.Image) -> bool:
    if image1.size != image2.size:
        return True

    # Ensure alpha channel
    if image1.mode != "RGBA":
        image1 = image1.convert("RGBA")
    if image2.mode != "RGBA":
        image2 = image2.convert("RGBA")
    
    pixels1 = image1.load()
    pixels2 = image2.load()

    for y in range(image1.height):
        for x in range(image1.width):
            pixel1 = pixels1[x, y]
            pixel2 = pixels2[x, y]

            # Ignore transparent pixels
            if pixel1[3] == 0 and pixel2[3] == 0:
                continue

            if pixel1 != pixel2:
                return True

    return False


def image_preview(image: Image.Image) -> None:
    # import time
    import os
    image.show()
    # time.sleep(2)
    print("Press ENTER to continue...")
    os.system("taskkill /f /im Photos.exe >nul 2>&1")