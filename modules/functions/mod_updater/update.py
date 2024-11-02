import json
import os
import shutil
import threading
from tempfile import TemporaryDirectory

from modules.logger import logger
from modules.request import RobloxApi
from modules import filesystem
from modules.functions.mod_updater import versions, path_to_imagesets, path_to_imagesetdata, icon_map, modded_icons, image_sets


def update_mods(data: dict, latest_version: str, output_dir: str) -> None:
    logger.debug(f"Updating mods: {data}")
    os.makedirs(output_dir, exist_ok=True)
    latest_player_version = versions.get_player_equivalent(latest_version) or latest_version
    latest_studio_version = versions.get_studio_equivalent(latest_version) or latest_version

    threads: list[threading.Thread] = []

    with TemporaryDirectory() as temp_directory:
        for git_hash, mods in data.items():
            print("Updating mods: "+str(", ".join([os.path.basename(mod) for mod in mods])))
            version_guid: str = versions.get_studio_version(git_hash=git_hash)

            thread: threading.Thread = threading.Thread(
                name="mod-updater-worker-thread",
                target=worker,
                kwargs={
                    "mod_studio_version": version_guid,
                    "mods": mods,
                    "latest_player_version": latest_player_version,
                    "latest_studio_version": latest_studio_version,
                    "temp_directory": temp_directory,
                    "output_dir": output_dir
                },
                daemon=True
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()



def worker(mod_studio_version: str, mods: list, latest_player_version: str, latest_studio_version: str, temp_directory: str, output_dir: str) -> None:
    if not mods:
        return

    try:
        logger.info("Copying mods and updating info.json . . .")
        for mod in mods:
            shutil.copytree(
                mod,
                os.path.join(temp_directory, os.path.basename(mod)),
                dirs_exist_ok=True
            )
            with open(os.path.join(temp_directory, os.path.basename(mod), "info.json"), "r") as file:
                data = json.load(file)
            data["clientVersionUpload"] = latest_player_version
            with open(os.path.join(temp_directory, os.path.basename(mod), "info.json"), "w") as file:
                json.dump(data, file, indent=4)

        print("Downloading LuaPackages . . .")
        download_threads: list[threading.Thread] = []
        versions_to_download: list[str] = [
            latest_studio_version,
            mod_studio_version
        ]
        for version in versions_to_download:
            thread = threading.Thread(
                name="mod-updater-file-download-thread",
                target=download_luapackages,
                kwargs={
                    "temp_directory": temp_directory,
                    "version": version
                },
                daemon=True
            )
            download_threads.append(thread)
            thread.start()

        old_imageset_basepath: str = path_to_imagesets.get(root=os.path.join(temp_directory, os.path.basename(mods[0]), "ExtraContent", "LuaPackages"))

        for thread in download_threads:
            thread.join()
        
        print("Locating ImageSets . . .")
        latest_version_path: str = os.path.join(temp_directory, latest_studio_version)
        new_imageset_basepath: str = path_to_imagesets.get(root=os.path.join(latest_version_path, "ExtraContent", "LuaPackages"))

        old_imagesetdata_path: str = path_to_imagesetdata.get(root=os.path.join(temp_directory, mod_studio_version, "ExtraContent", "LuaPackages"))
        new_imagesetdata_path: str = path_to_imagesetdata.get(root=os.path.join(temp_directory, latest_version_path, "ExtraContent", "LuaPackages"))

        old_icon_map: dict[str,dict[str,dict[str,str|int]]] = icon_map.get(path=os.path.join(temp_directory, mod_studio_version, "ExtraContent", "LuaPackages", old_imagesetdata_path))
        new_icon_map: dict[str,dict[str,dict[str,str|int]]] = icon_map.get(path=os.path.join(latest_version_path, "ExtraContent", "LuaPackages", new_imagesetdata_path))

        for mod in mods:
            print("Detecting modded icons . . .")
            logger.info("Detecting modded icons . . .")
            modded_icon_data: dict[str,list[str]] = modded_icons.get(
                mod_path=os.path.join(temp_directory, os.path.basename(mod)),
                version_path=os.path.join(temp_directory, mod_studio_version),
                imageset_path=os.path.join("ExtraContent", "LuaPackages", old_imageset_basepath),
                icon_map=old_icon_map
            )
            if modded_icon_data == modded_icons.DEFAULT:
                continue

            print("Generating ImageSets . . .")
            logger.info("Generating ImageSets . . .")
            image_sets.generate(
                temp_directory=temp_directory,
                mod=os.path.basename(mod),
                version=latest_studio_version,
                old_imageset_path=os.path.join("ExtraContent", "LuaPackages", old_imageset_basepath),
                new_imageset_path=os.path.join("ExtraContent", "LuaPackages", new_imageset_basepath),
                modded_icons=modded_icon_data,
                old_icon_map=old_icon_map,
                new_icon_map=new_icon_map
            )

            print("Finishing mod update . . .")
            shutil.rmtree(os.path.join(output_dir, mod), ignore_errors=True)
            os.makedirs(os.path.join(output_dir, mod), exist_ok=True)
            shutil.copytree(
                os.path.join(temp_directory, os.path.basename(mod)),
                os.path.join(output_dir, os.path.basename(mod)),
                dirs_exist_ok=True
            )


    except Exception as e:
        logger.warning("mod updater thread failed!")
        logger.error(type(e).__name__+": "+str(e))
        print("mod updater thread! "+type(e).__name__+": "+str(e))


def download_luapackages(temp_directory, version: str) -> None:
    logger.info("Downloading LuaPackages")

    filesystem.download(
        url=RobloxApi.download(version=version, file="extracontent-luapackages.zip"),
        destination=os.path.join(temp_directory, version+"-extracontent-luapackages.zip")
    )
    filesystem.extract(
        source=os.path.join(temp_directory, version+"-extracontent-luapackages.zip"),
        destination=os.path.join(temp_directory, version, "ExtraContent", "LuaPackages")
    )
    os.remove(os.path.join(temp_directory, version+"-extracontent-luapackages.zip"))