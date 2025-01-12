from pathlib import Path
import json
import sys

from modules import Logger
from modules.filesystem import Directory

from .get_mask import get_mask

from PIL import Image


def generate_additional_files(base_directory: Path, color1, color2, angle: int) -> None:
    if getattr(sys, "frozen", False):
        mod_generator_files: Path = Path(sys._MEIPASS, "mod_generator_files")
    else:
        mod_generator_files = Directory.ROOT / "modules" / "mod_generator" / "additional_files"
    index_filepath: Path = mod_generator_files / "index.json"

    if not index_filepath.is_file():
        Logger.warning("Cannot generate additional files! index.json does not exist!")
        return
    
    with open(index_filepath, "r") as file:
        data: dict = json.load(file)
    
    for filepath in mod_generator_files.iterdir():
        if filepath.name == index_filepath.name:
            continue
        
        target: list[str] | None = data.get(filepath.name)
        print(target)
        if not target or not isinstance(target, list):
            Logger.warning(f"Cannot generate additional file: {filepath.name}! Unknown target path!")
            continue

        target_path: Path = Path(base_directory, *target)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with Image.open(filepath, formats=("PNG",)) as image:
            image = image.convert("RGBA")
            r, g, b, a = image.split()

        modded_icon = get_mask(color1, color2, angle, image.size)
        modded_icon.putalpha(a)
        modded_icon.save(target_path, format="PNG", optimize=False)