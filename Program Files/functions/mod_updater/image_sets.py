import os
import shutil

from PIL import Image


def generate(temp_directory, mod: str, version: str, old_imageset_path: str, new_imageset_path: str, modded_icons: dict[str,list[str]], icon_map: dict[str,dict[str,dict[str,str|int]]]) -> None:
    mod_path: str = os.path.join(temp_directory, mod)
    old_path: str = os.path.join(mod_path, old_imageset_path)
    new_path: str = os.path.join(mod_path, new_imageset_path)
    version_path: str = os.path.join(temp_directory, version, new_imageset_path)

    shutil.copytree(old_path, os.path.join(temp_directory, "mod_imagesets"))
    shutil.rmtree(old_path)
    if old_path != new_path:
        while True:
            old_path: str = os.path.dirname(old_path)
            if old_path == mod_path:
                break
            with os.scandir(old_path) as entries:
                if not any(entries):
                    os.rmdir(old_path)
                else:
                    break
    shutil.copytree(version_path, new_path)

    for size, icons in modded_icons.items():
        for name in icons:
            data: dict = icon_map[size][name]
            
            path: str = os.path.join(new_path, str(data["set"]))+".png"
            modded_path: str = os.path.join(temp_directory, "mod_imagesets", str(data["set"]))+".png"
            
            x: int = int(data["x"])
            y: int = int(data["y"])
            w: int = int(data["w"])
            h: int = int(data["h"])

            with Image.open(path) as imageset:
                with Image.open(modded_path) as modded_imageset:
                    modded_icon = modded_imageset.crop((x,y,x+w,y+h))
                imageset.paste(modded_icon, (x,y,x+w,y+h))
                imageset.save(path)