import json
import os
import sys
import shutil
import time
from tempfile import TemporaryDirectory

python_version: str = str(sys.version_info.major)+"."+str(sys.version_info.minor)
libraries: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "libraries", python_version)
modules: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "modules")

sys.path.append(libraries)
sys.path.append(modules)
sys.path.append(os.path.dirname(modules))

try:
    from modules import filesystem, request, exception_handler
    from modules.interface import Color, Response
    from main import WELCOME_MESSAGE
    from modules.functions import latest_roblox_version, mod_updater

except Exception as e:
    print("Mod download failed!")
    print(str(type(e).__name__)+": "+str(e))
    input("Press ENTER to close . . .")
    sys.exit()


USER_CHANNEL_DEFAULT: str = "LIVE"
BINARY_TYPE: str = "WindowsPlayer"


def main() -> None:
    try:
        args: list = sys.argv[1:]
        if args == []:
            raise Exception("No arguments given")

        mod_id: str = str(args[0])
        mod_name: str = str(args[1])
        print(Color.SPLASH+WELCOME_MESSAGE)
        print(Color.INFO+"Downloading mod: "+Color.INITIALIZE+mod_name+Color.RESET)
        print()

        print(Color.INFO+"Checking for existing installations . . ."+Color.RESET)
        if mod_exists(mod_name):
            print("Mod already exists, do you still wish to continue? [Y/N]")
            while True:
                response: str = input("Response: ").lower()

                if response in Response.ACCEPT:
                    break

                elif response in Response.DENY:
                    print()
                    print(Color.WARNING+"Mod download cancelled!", end="")
                    close_window()
                
                print("bad input: \""+response+"\"")
                print("Response must be yes or no")
            print()

        with TemporaryDirectory() as temp_directory:
            print(Color.INFO+"Downloading mod . . ."+Color.RESET)
            filesystem.download(
                url=request.Api.mod_download(id=mod_id),
                destination=os.path.join(temp_directory, mod_id)
            )

            target: str = os.path.join(filesystem.Directory.mods(), mod_name)
            print(Color.INFO+"Extracting mod . . ."+Color.RESET)
            if os.path.isdir(target):
                shutil.rmtree(target, ignore_errors=True)
            filesystem.extract(
                source=os.path.join(temp_directory, mod_id),
                destination=target
            )

            print(Color.INFO+"Copying files . . ."+Color.RESET)
        
        print(Color.INFO+"Checking for updates . . ."+Color.RESET)
        if is_updated(mod=mod_name) == False:
            update_mod(mod=mod_name)
        
        print(Color.INFO+"Mod download complete!")
        close_window()
    
    except Exception as e:
        exception_handler.run(e)


def close_window(seconds: int = 3) -> None:
    print()
    for i in range(seconds, 0, -1):
        print(Color.INITIALIZE+"Closing in "+Color.ACTION+str(i)+Color.RESET+" . . .", end="\r")
        time.sleep(1)
    sys.exit()


def mod_exists(mod: str) -> bool:
    path: str = os.path.join(filesystem.Directory.mods(), mod)
    return os.path.isdir(path)


def mod_version(mod: str, directory: str|None = None) -> str|None:
    path: str = os.path.join(directory or filesystem.Directory.mods(), mod, "info.json")
    if not os.path.isfile(path):
        return None
    with open(path, "r") as file:
        data = json.load(file)
        mod_version: str = data.get("clientVersionUpload", None)
    return mod_version


def is_updated(mod: str, directory: str|None = None) -> bool:
    version: str|None = mod_version(mod=mod, directory=directory)
    if not version:
        return True
    
    latest_version: str = latest_roblox_version.get(binary_type=BINARY_TYPE)
    return latest_version == version


def update_mod(mod: str) -> None:
    print()
    print(Color.INITIALIZE+"Updating mod . . ."+Color.RESET)

    try:
        print(Color.INFO+"Comparing versions . . ."+Color.RESET)
        version: str|None = mod_version(mod=mod)
        if not version:
            raise Exception("Failed to get version info")
        latest_version: str = latest_roblox_version.get(binary_type=BINARY_TYPE)

        studio_version: str|None = mod_updater.versions.get_studio_equivalent(guid=version)
        latest_studio_version: str|None = mod_updater.versions.get_studio_equivalent(guid=latest_version)

        if not studio_version or not latest_studio_version:
            raise Exception("Failed to get Studio equivalent!")

        print(Color.INFO+"\u2022 "+Color.INITIALIZE+"Mod version: "+Color.ACTION+str(version)+", "+str(studio_version))
        print(Color.INFO+"\u2022 "+Color.INITIALIZE+"Latest Roblox version: "+Color.ACTION+str(latest_version)+", "+str(latest_studio_version))
        
        with TemporaryDirectory() as temp_directory:
            luapackages_basepath: str = os.path.join("ExtraContent", "LuaPackages")

            print(Color.INFO+"Downloading LuaPackages (1/2). . ."+Color.RESET)
            filesystem.download(
                url=request.RobloxApi.download(
                    version=studio_version,
                    file="extracontent-luapackages.zip"
                ),
                destination=os.path.join(temp_directory, "extracontent-luapackages.zip")
            )
            filesystem.extract(
                source=os.path.join(temp_directory, "extracontent-luapackages.zip"),
                destination=os.path.join(temp_directory, studio_version, luapackages_basepath)
            )
            filesystem.remove(path=os.path.join(temp_directory, "extracontent-luapackages.zip"))

            print(Color.INFO+"Downloading LuaPackages (2/2). . ."+Color.RESET)
            filesystem.download(
                url=request.RobloxApi.download(
                    version=latest_studio_version,
                    file="extracontent-luapackages.zip"
                ),
                destination=os.path.join(temp_directory, "extracontent-luapackages.zip")
            )
            filesystem.extract(
                source=os.path.join(temp_directory, "extracontent-luapackages.zip"),
                destination=os.path.join(temp_directory, latest_studio_version, luapackages_basepath)
            )
            filesystem.remove(path=os.path.join(temp_directory, "extracontent-luapackages.zip"))

            shutil.copytree(
                src=os.path.join(filesystem.Directory.mods(), mod),
                dst=os.path.join(temp_directory, mod),
                dirs_exist_ok=True
            )

            print(Color.INFO+"Locating ImageSets . . ."+Color.RESET)
            path_to_imagesets_old: str = mod_updater.path_to_imagesets.get(root=os.path.join(temp_directory, mod))
            path_to_imagesets_new: str = mod_updater.path_to_imagesets.get(root=os.path.join(temp_directory, studio_version))

            print(Color.INFO+"Locating GetImageSetData.lua . . ."+Color.RESET)
            path_to_imagesetdata_old: str = mod_updater.path_to_imagesetdata.get(root=os.path.join(temp_directory, studio_version))
            path_to_imagesetdata_new: str = mod_updater.path_to_imagesetdata.get(root=os.path.join(temp_directory, latest_studio_version))

            print(Color.INFO+"Reading icon data . . ."+Color.RESET)
            icon_map_old: dict[str,dict[str,dict[str,str|int]]] = mod_updater.icon_map.get(
                path=os.path.join(temp_directory, studio_version, path_to_imagesetdata_old)
            )
            icon_map_new: dict[str,dict[str,dict[str,str|int]]] = mod_updater.icon_map.get(
                path=os.path.join(temp_directory, latest_studio_version, path_to_imagesetdata_new)
            )

            print(Color.INFO+"Detecting modded icons . . ."+Color.RESET)
            modded_icons: dict[str,list[str]] = mod_updater.modded_icons.get(
                mod_path=os.path.join(temp_directory, mod),
                version_path=os.path.join(temp_directory, studio_version),
                imageset_path=path_to_imagesets_old,
                icon_map=icon_map_old
            )
            if modded_icons == mod_updater.modded_icons.DEFAULT:
                print(Color.WARNING+"No modded icons detected!"+Color.RESET)
                close_window()

            print(Color.INFO+"Generating ImageSets . . ."+Color.RESET)
            mod_updater.image_sets.generate(
                temp_directory=temp_directory,
                mod=mod,
                version=latest_studio_version,
                old_imageset_path=path_to_imagesets_old,
                new_imageset_path=path_to_imagesets_new,
                modded_icons=modded_icons,
                icon_map=icon_map_new
            )

            print(Color.INFO+"Copying files . . ."+Color.RESET)
            shutil.rmtree(os.path.join(filesystem.Directory.mods(), mod), ignore_errors=True)
            shutil.copytree(os.path.join(temp_directory, mod), os.path.join(filesystem.Directory.mods(), mod), dirs_exist_ok=True)

        print(Color.INFO+"Finishing mod update . . ."+Color.RESET)
        info_path: str = os.path.join(filesystem.Directory.mods(), mod, "info.json")
        data: dict = {}
        if os.path.isfile(info_path):
            with open(info_path, "r") as file:
                data = json.load(file)
        data["clientVersionUpload"] = latest_version
        with open(info_path, "w") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        print()
        print(Color.ERROR+"Mod update Failed!"+Color.RESET)
        print(Color.ERROR+type(e).__name__+": "+Color.WARNING+str(e)+Color.RESET)
        print()
        return


if __name__ == '__main__':
    main()