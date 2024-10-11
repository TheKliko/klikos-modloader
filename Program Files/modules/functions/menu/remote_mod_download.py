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
    from modules.functions.mod_updater import check_for_mod_updates, update_mods

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
                destination=os.path.join(temp_directory, mod_id+".zip")
            )

            target: str = os.path.join(filesystem.Directory.mods(), mod_name)
            print(Color.INFO+"Extracting mod . . ."+Color.RESET)
            if os.path.isdir(target):
                shutil.rmtree(target, ignore_errors=True)
            filesystem.extract(
                source=os.path.join(temp_directory, mod_id+".zip"),
                destination=target
            )

            print(Color.INFO+"Copying files . . ."+Color.RESET)
        
        print(Color.INFO+"Checking for updates . . ."+Color.RESET)
        latest_version: str = latest_roblox_version.get(binary_type=BINARY_TYPE)
        mod_update_check = check_for_mod_updates(mods=[mod_name], latest_version=latest_version)
        if mod_update_check != False:
            print(Color.INFO+"Updating mod . . ."+Color.RESET)
            update_mods(data=mod_update_check, latest_version=latest_version)
        
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


def mod_version(mod: str) -> str|None:
    path: str = os.path.join(filesystem.Directory.mods(), mod, "info.json")
    if not os.path.isfile(path):
        return None
    with open(path, "r") as file:
        data = json.load(file)
        mod_version: str = data.get("clientVersionUpload", None)
    return mod_version


def is_updated(mod: str) -> bool:
    version: str|None = mod_version(mod=mod)
    if not version:
        return True
    
    latest_version: str = latest_roblox_version.get(binary_type=BINARY_TYPE)
    return latest_version == version


if __name__ == '__main__':
    main()