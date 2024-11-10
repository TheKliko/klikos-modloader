import os
import shutil
from modules.logger import logger
import threading

from PIL import Image


def generate(temp_directory, mod: str, version: str, old_imageset_path: str, new_imageset_path: str, modded_icons: dict[str,list[str]], old_icon_map: dict[str,dict[str,dict[str,str|int]]], new_icon_map: dict[str,dict[str,dict[str,str|int]]]) -> None:
    common_imageset_data: dict[str,list[dict]] = {}
    uncommon_imageset_data: list[dict] = []
    modded_imagesets: list[str] = []
    
    
    mod_path: str = os.path.join(temp_directory, mod)
    old_path: str = os.path.join(mod_path, old_imageset_path)
    new_path: str = os.path.join(mod_path, new_imageset_path)
    version_path: str = os.path.join(temp_directory, version, new_imageset_path)

    shutil.copytree(old_path, os.path.join(temp_directory, f"mod_imagesets_{mod}"))
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
            if old_icon_map.get(size, {}).get(name) is None:
                logger.warning(f"ImageSet generator, key not found in {size}: {name}")
                continue
            if new_icon_map.get(size, {}).get(name) is None:
                logger.warning(f"ImageSet generator, key not found in {size}: {name}")
                continue

            old_data: dict = old_icon_map[size][name]
            new_data: dict = new_icon_map[size][name]
            
            old_imageset_name: str = str(old_data["set"])+".png"
            new_imageset_name: str = str(new_data["set"])+".png"
            
            if new_imageset_name not in modded_imagesets:
                modded_imagesets.append(new_imageset_name)
            
            old_x: int = int(old_data["x"])
            old_y: int = int(old_data["y"])
            old_w: int = int(old_data["w"])
            old_h: int = int(old_data["h"])
            
            new_x: int = int(new_data["x"])
            new_y: int = int(new_data["y"])
            new_w: int = int(new_data["w"])
            new_h: int = int(new_data["h"])

            if old_imageset_name == new_imageset_name:
                if old_imageset_name not in common_imageset_data:
                    common_imageset_data[old_imageset_name] = []
                common_imageset_data[old_imageset_name].append(
                    {
                        "old": {
                            "y": old_y,
                            "x": old_x,
                            "w": old_w,
                            "h": old_h
                        },
                        "new": {
                            "y": new_y,
                            "x": new_x,
                            "w": new_w,
                            "h": new_h
                        }
                    }
                )

            else:
                uncommon_imageset_data.append(
                    {
                        "old": {
                            "set": old_imageset_name,
                            "y": old_y,
                            "x": old_x,
                            "w": old_w,
                            "h": old_h
                        },
                        "new": {
                            "set": new_imageset_name,
                            "y": new_y,
                            "x": new_x,
                            "w": new_w,
                            "h": new_h
                        }
                    }
                )

    update_common_imagesets(temp_directory=temp_directory, new_path=new_path, mod=mod, common_imageset_data=common_imageset_data)
    update_uncommon_imagesets(temp_directory=temp_directory, new_path=new_path, mod=mod, uncommon_imageset_data=uncommon_imageset_data)
    delete_unmodded_imagesets(temp_directory=temp_directory, path_extension=new_path, modded_imagesets=modded_imagesets)


def update_common_imagesets(temp_directory: str, new_path: str, mod: str, common_imageset_data: dict[str, list[dict]]) -> None:
    threads: list[threading.Thread] = []

    def worker(path: str, modded_path: str, icons: list[dict]) -> None:
            with Image.open(path).convert("RGBA") as imageset:
                with Image.open(modded_path).convert("RGBA") as modded_imageset:
                        for icon in icons:
                            old_x: int = int(icon["old"]["x"])
                            old_y: int = int(icon["old"]["y"])
                            old_w: int = int(icon["old"]["w"])
                            old_h: int = int(icon["old"]["h"])

                            new_x: int = int(icon["new"]["x"])
                            new_y: int = int(icon["new"]["y"])
                            new_w: int = int(icon["new"]["w"])
                            new_h: int = int(icon["new"]["h"])

                            modded_icon = modded_imageset.crop((old_x,old_y,old_x+old_w,old_y+old_h))
                            imageset.paste(modded_icon, (new_x,new_y,new_x+new_w,new_y+new_h))
                        imageset.save(path, format="PNG", optimize=False)

    for imageset_name, data in common_imageset_data.items():
        path: str = os.path.join(new_path, imageset_name)
        modded_path: str = os.path.join(temp_directory, f"mod_imagesets_{mod}", imageset_name)

        thread = threading.Thread(
            name="imageset-generator-thread",
            target=worker,
            kwargs={
                "path": path,
                "modded_path": modded_path,
                "icons": data
            }
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def update_uncommon_imagesets(temp_directory: str, new_path: str, mod: str, uncommon_imageset_data: list[dict]) -> None:
    for data in uncommon_imageset_data:
        old_data: dict = data["old"]
        new_data: dict = data["new"]

        modded_path: str = os.path.join(temp_directory, f"mod_imagesets_{mod}", old_data["set"])
        target_path: str = os.path.join(new_path, new_data["set"])

        old_x: int = int(old_data["x"])
        old_y: int = int(old_data["y"])
        old_w: int = int(old_data["w"])
        old_h: int = int(old_data["h"])

        new_x: int = int(new_data["x"])
        new_y: int = int(new_data["y"])
        new_w: int = int(new_data["w"])
        new_h: int = int(new_data["h"])

        with Image.open(modded_path).convert("RGBA") as modded_imageset:
            modded_icon = modded_imageset.crop((old_x,old_y,old_x+old_w,old_y+old_h))

        with Image.open(target_path).convert("RGBA") as imageset:
            imageset.paste(modded_icon, (new_x,new_y,new_x+new_w,new_y+new_h))
            imageset.save(target_path, format="PNG", optimize=False)


def delete_unmodded_imagesets(temp_directory: str, path_extension: str, modded_imagesets: list[str]) -> None:
    path_to_imagesets: str = os.path.join(temp_directory, path_extension)
    
    if not os.path.exists(path_to_imagesets):
        return
    
    for file in os.listdir(path_to_imagesets):
        path = os.path.join(path_to_imagesets, file)
        if os.path.isfile(path) and file not in modded_imagesets:
            try:
                os.remove(path)
            except:
                pass