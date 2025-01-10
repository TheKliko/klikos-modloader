from pathlib import Path

from PIL import Image, PngImagePlugin


def add_watermark(mod_imagesets_directory: Path) -> None:
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Text", "Generated with Kliko's mod generator")

    for filepath in mod_imagesets_directory.iterdir():
        if not filepath.is_file() or not filepath.suffix == ".png":
            continue
        
        with Image.open(filepath, formats=("PNG",)) as image:
            image.save(filepath, format="PNG", optimize=False, pnginfo=metadata)