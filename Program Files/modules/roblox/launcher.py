import logging
import os
import subprocess
import threading
import time

from modules.other.paths import Directory
from modules.utils import variables


def launch(binary_type: str, version: str) -> None:
    base_path: str = os.path.join(Directory.VERSIONS, version)
    executable: str = f'Roblox{binary_type.removeprefix('Windows')}Beta.exe'
    file_path: str = os.path.join(base_path, executable)

    command: str = f'"{file_path}" '
    launch_args: str = variables.get('launch_arguments', None)
    if launch_args:
        launch_args = '+'.join([f'launchtime:{int(time.time()*1000)}' if item.startswith('launchtime:') else item for item in launch_args.split('+')])
        command += launch_args

    logging.info(f'Launching {executable}')
    subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )