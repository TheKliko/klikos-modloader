from pathlib import Path
import shutil

from PIL import Image


def generate_new_imagesets(modded_icons: dict[str, list[str]], mod_icon_map: dict[str, dict[str, dict[str, str | int]]], latest_icon_map: dict[str, dict[str, dict[str, str | int]]], mod_imageset_path: Path, latest_imageset_path: Path, latest_version: str, mod: str, temporary_directory: Path) -> None:
    shutil.copytree(temporary_directory / mod / mod_imageset_path, temporary_directory / f"{mod}_old_imagesets")
    shutil.rmtree(temporary_directory / mod / mod_imageset_path)

    # Remove empty directories leading up to the ImageSets (in case the ImageSets get moved to somewhere else)
    for parent in (temporary_directory / mod / mod_imageset_path).parents:
        if parent == (temporary_directory / mod):
            break
        if not any(parent.iterdir()):
            parent.rmdir()
        else:
            break
    
    shutil.copytree(temporary_directory / latest_version / latest_imageset_path, temporary_directory / mod / latest_imageset_path, dirs_exist_ok=True)

    # Copy the modded icons to the new ImageSets
    modded_imagesets: list[str] = []
    shared_atlas_icons: dict[str, dict[str, list[str]]] = {}
    atlas_hopped_icons: dict[str, list[str]] = {}

    for size, icons in modded_icons.items():
        for icon in icons:
            old_image_set: str = mod_icon_map[size][icon]["image_set"]
            new_image_set: str = latest_icon_map[size][icon]["image_set"]

            if old_image_set == new_image_set:
                if size not in shared_atlas_icons:
                    shared_atlas_icons[size] = {}
                if new_image_set not in shared_atlas_icons[size]:
                    shared_atlas_icons[size][new_image_set] = []
                shared_atlas_icons[size][new_image_set].append(icon)
            
            else:
                if size not in atlas_hopped_icons:
                    atlas_hopped_icons[size] = []
                atlas_hopped_icons[size].append(icon)
            
            if new_image_set not in modded_imagesets:
                modded_imagesets.append(f"{new_image_set}.png")
    
    for size, imagesets in shared_atlas_icons.items():
        for image_set, icons in imagesets.items():
            modded_path: Path = (temporary_directory / f"{mod}_old_imagesets" / image_set).with_suffix(".png")
            new_path: Path = (temporary_directory / mod / latest_imageset_path / image_set).with_suffix(".png")

            with Image.open(modded_path, formats=("PNG",)) as modded_image:
                modded_image = modded_image.convert("RGBA")

                with Image.open(new_path, formats=("PNG",)) as new_image:
                    new_image = new_image.convert("RGBA")

                    for icon in icons:
                        old_x: int = mod_icon_map[size][icon]["x"]
                        old_y: int = mod_icon_map[size][icon]["y"]
                        old_w: int = mod_icon_map[size][icon]["w"]
                        old_h: int = mod_icon_map[size][icon]["h"]
                        
                        new_x: int = latest_icon_map[size][icon]["x"]
                        new_y: int = latest_icon_map[size][icon]["y"]
                        new_w: int = latest_icon_map[size][icon]["w"]
                        new_h: int = latest_icon_map[size][icon]["h"]

                        modded_icon: Image.Image = modded_image.crop((old_x, old_y, old_x + old_w, old_y + old_h))
                        new_image.paste(modded_icon, (new_x, new_y, new_x + new_w, new_y + new_h))
                    new_image.save(new_path, format="PNG", optimize=False)
    
    for size, icons in atlas_hopped_icons.items():
        for icon in icons:
            old_image_set: str = mod_icon_map[size][icon]["image_set"]
            new_image_set: str = latest_icon_map[size][icon]["image_set"]

            modded_path: Path = (temporary_directory / f"{mod}_old_imagesets" / old_image_set).with_suffix(".png")
            new_path: Path = (temporary_directory / mod / latest_imageset_path / new_image_set).with_suffix(".png")

            old_x: int = mod_icon_map[size][icon]["x"]
            old_y: int = mod_icon_map[size][icon]["y"]
            old_w: int = mod_icon_map[size][icon]["w"]
            old_h: int = mod_icon_map[size][icon]["h"]

            new_x: int = latest_icon_map[size][icon]["x"]
            new_y: int = latest_icon_map[size][icon]["y"]
            new_w: int = latest_icon_map[size][icon]["w"]
            new_h: int = latest_icon_map[size][icon]["h"]

            with Image.open(modded_path, formats=("PNG",)) as modded_image:
                modded_image = modded_image.convert("RGBA")
                modded_icon: Image.Image = modded_image.crop((old_x, old_y, old_x + old_w, old_y + old_h))

            with Image.open(new_path, formats=("PNG",)) as new_image:
                new_image = new_image.convert("RGBA")
                new_image.paste(modded_icon, (new_x, new_y, new_x + new_w, new_y + new_h))
                new_image.save(new_path, format="PNG", optimize=False)
    
    # Remove unmodded ImageSets
    for item in (temporary_directory / mod / latest_imageset_path).iterdir():
        if item.is_file() and item.name not in modded_imagesets:
            item.unlink()