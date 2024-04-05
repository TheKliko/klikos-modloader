import os
import sys
import platform
import logging


global root_directory, logging_directory, config_directory, default_config, user_directory
root_directory: str = os.path.dirname(os.path.dirname(__file__))
logging_directory: str = os.path.join(root_directory, 'Logs')
config_directory: str = os.path.join(root_directory, 'Program Files', 'config')
user_directory: str = os.path.join(root_directory, 'User Profiles')

default_config: str = r'https://raw.githubusercontent.com/TheKliko/roblox-modloader/main/Program%20Files/config/config.json'
default_config: str = r'https://raw.githubusercontent.com/TheKliko/testing/main/config.json' # REMOVE BEFORE RELEASE



def system_not_supported() -> None:
    print(f'This program is not supported on {platform.system()}.')
    input('press ENTER to exit')

def get_launch_arguments() -> str | None:
    try:
        launch_argument: str | None = str(sys.argv[1][1:])
    except:
        launch_argument = None
    return launch_argument

def run_launcher_process(version_directory: str) -> None:
    from modules.launcher_process import launcher
    launcher(version_directory=version_directory)

def run_setup_process() -> None:
    from modules.setup_process import setup
    setup()

def run_info_process() -> None:
    from modules.info_process import info
    info()

def main() -> None:
    if not platform.system() == 'Windows':
        system_not_supported()
        return
    
    from modules.initialization import initialize
    initialize()

    launch_arguments = get_launch_arguments()
    if launch_arguments == 'launcher':
        from modules.initialization import version_directory
        run_launcher_process(version_directory=version_directory)
    elif launch_arguments == 'setup':
        run_setup_process()
    elif launch_arguments == 'info':
        run_info_process()
    else:
        logging.warning(f'Invalid launch argument(s): {str(launch_arguments)}')

    from modules.basic_functions import terminate
    terminate(timer=5)
    print('e')
    input()

if __name__ == '__main__':
    main()