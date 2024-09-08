import logging
import os
import importlib.util

from modules.other.paths import Directory
from modules.utils import variables

from .install import install


IMPORT_MAP: dict = {
    'pillow': 'PIL'
}


def check_version_specific_libraries(version_specific_libraries: list[str]) -> None:
    python_version: str = variables.get('python_version')
    version_specific_library_directory: str = os.path.join(Directory.PROGRAM_FILES, 'version_specific_libraries', f'python-{python_version}')
        
    if not os.path.isdir(version_specific_library_directory):
        os.makedirs(version_specific_library_directory)

    for library in version_specific_libraries:
        if not importlib.util.find_spec(IMPORT_MAP.get(library.lower(), library)):
            install(library, is_version_specific=True)

    try:
        if os.listdir(version_specific_library_directory) == []:
            os.rmdir(version_specific_library_directory)
            if os.listdir(os.path.dirname(version_specific_library_directory)) == []:
                os.rmdir(os.path.dirname(version_specific_library_directory))
    except Exception as e:
        logging.warning(f'Failed to remove version_specific_library_directory: {str(e)}')