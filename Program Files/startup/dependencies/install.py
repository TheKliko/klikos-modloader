import logging
import os
import subprocess
import sys

from modules.interface import Color
from modules.filesystem.directories import Directory
from modules import filesystem
from modules import variables


IMPORT_MAP: dict = {
    "PIL": "pillow",
    "notifypy": "notify-py"
}


def install(library: str) -> None:
    logging.debug(f"Installing dependency: {library}")

    library_directory: str = os.path.join(Directory.program_files(), "libraries", variables.get("python_version"))
    
    filesystem.verify(library_directory, create_missing_directories=True)

    install_path: str = library_directory
    
    try:
        print(Color.WARNING+" Installing dependency: "+library)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--target", install_path, "--upgrade", IMPORT_MAP.get(library, library)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    
    except subprocess.CalledProcessError as e:
        logging.error(type(e).__name__+": "+str(e))
        raise Exception(str(e))