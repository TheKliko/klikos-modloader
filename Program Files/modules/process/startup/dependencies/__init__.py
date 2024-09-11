import json
import logging
import os
import sys

from modules.interface import Print, Color
from modules.other.paths import Directory
from modules.utils import variables

from .is_installed import is_installed
from .install import install
from .check_version_specific_libraries import check_version_specific_libraries


def check_dependencies() -> None:
    try:
        logging.debug(f'Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}-{sys.version_info.releaselevel}')
        logging.info('Checking dependencies . . .')
        Print('Checking dependencies . . .', color=Color.INITALIZE)

        with open(os.path.join(os.path.dirname(__file__), 'requirements.json'), 'r') as file:
            data: dict = json.load(file)
            file.close()

        normal: list[str] = data.get('normal', [])
        version_specific: list[str] = data.get('version_specific', [])


        for library in normal:
            if is_installed(library) == False:
                install(library)
            else:
                continue

        check_version_specific_libraries(version_specific)
    
    except Exception as e:
        logging.error(f'[DependencyError] [{type(e).__name__}] {str(e)}')