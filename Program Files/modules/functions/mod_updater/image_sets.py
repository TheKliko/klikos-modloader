import os
import shutil
import threading

from PIL import Image


threads: list[threading.Thread] = []
imageset_data: dict = {}


def generate(temp_directory, mod: str, version: str, old_imageset_path: str, new_imageset_path: str, modded_icons: dict[str,list[str]], icon_map: dict[str,dict[str,dict[str,str|int]]]) -> None:
    global imageset_data
    global threads
    
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
            
            imageset_name: str = str(data["set"])+".png"
            
            x: int = int(data["x"])
            y: int = int(data["y"])
            w: int = int(data["w"])
            h: int = int(data["h"])

            if imageset_name not in imageset_data:
                imageset_data[imageset_name] = []
            imageset_data[imageset_name].append(
                {
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h
                }
            )
    update_imagesets(temp_directory=temp_directory, new_path=new_path)
    delete_unmodded_imagesets(temp_directory=temp_directory, path_extension=new_path)



def update_imagesets(temp_directory: str, new_path: str) -> None:
    global imageset_data
    global threads

    def worker(path: str, modded_path: str, icons: list[dict]) -> None:
            with Image.open(path) as imageset:
                with Image.open(modded_path) as modded_imageset:
                        for icon in icons:
                            x: int = int(icon["x"])
                            y: int = int(icon["y"])
                            w: int = int(icon["w"])
                            h: int = int(icon["h"])
                            modded_icon = modded_imageset.crop((x,y,x+w,y+h))
                            imageset.paste(modded_icon, (x,y,x+w,y+h))
                        imageset.save(path)

    for imageset_name, data in imageset_data.items():
        path: str = os.path.join(new_path, imageset_name)
        modded_path: str = os.path.join(temp_directory, "mod_imagesets", imageset_name)

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


def delete_unmodded_imagesets(temp_directory: str, path_extension: str) -> None:
    global imageset_data

    path_to_imagesets: str = os.path.join(temp_directory, path_extension)
    imageset_names = set(imageset_data.keys())
    
    if not os.path.exists(path_to_imagesets):
        return
    
    for file in os.listdir(path_to_imagesets):
        path = os.path.join(path_to_imagesets, file)
        if os.path.isfile(path) and file not in imageset_names:
            try:
                os.remove(path)
            except:
                pass