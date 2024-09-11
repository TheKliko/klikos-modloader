import logging
import os
import subprocess
import sys

from modules.interface import Print, Color
from modules.other.paths import Directory
from modules.utils import filesystem
from modules.utils import variables


IMPORT_MAP: dict = {
    'PIL': 'pillow',
    'notifypy': 'notify-py'
}


def install(library: str, is_version_specific: bool = False) -> None:
    logging.debug(f'Installing dependency: {library}')

    library_directory: str = os.path.join(Directory.PROGRAM_FILES, 'libraries')
    version_specific_library_directory: str = os.path.join(Directory.PROGRAM_FILES, 'version_specific_libraries', f'python-{variables.get('python_version')}')
    
    filesystem.verify(library_directory, create_missing_directories=True)
    filesystem.verify(version_specific_library_directory, create_missing_directories=True)

    install_path: str = library_directory if is_version_specific == False else version_specific_library_directory
    
    try:
        Print(f'Installing dependency: {library}', color=Color.WARNING, indent=2)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--target', install_path, '--upgrade', IMPORT_MAP.get(library.lower(), library)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        logging.error(f'[DependencyError] [{type(e).__name__}] Failed to install dependency: {str(e)}')
        raise Exception(f'[DependencyError] [{type(e).__name__}] Failed to install dependency: {str(e)}')