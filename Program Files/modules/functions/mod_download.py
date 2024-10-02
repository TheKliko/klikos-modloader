import os
import sys
from tempfile import TemporaryDirectory

python_version: str = str(sys.version_info.major)+"."+str(sys.version_info.minor)
libraries: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "libraries", python_version)
modules: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "modules")
os.makedirs(libraries, exist_ok=True)
sys.path.append(libraries)
sys.path.append(modules)
sys.path.append(os.path.dirname(modules))

try:
    from modules import filesystem, request, exception_handler
    from modules.interface import Color
    from main import WELCOME_MESSAGE

except Exception as e:
    print("Mod download failed!")
    print(str(type(e).__name__)+": "+str(e))
    input("Press ENTER to close . . .")

def main() -> None:
    try:
        args: list = sys.argv[1:]
        if args == []:
            raise Exception("No arguments given")
        
        mod: str = args[0]
        print(Color.SPLASH+WELCOME_MESSAGE)
        print(Color.INFO+"Downloading mod: "+Color.INITIALIZE+mod)
        print(Color.RESET)
        input(mod)

        with TemporaryDirectory() as temp_directory:
            input(temp_directory)
        raise NotImplementedError("mod_download.py")
    
    except Exception as e:
        exception_handler.run(e)


if __name__ == '__main__':
    main()