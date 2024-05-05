import os
import sys
import platform
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))

global root_directory, logging_directory, config_directory, default_config
root_directory: str = os.path.dirname(os.path.dirname(__file__))
logging_directory: str = os.path.join(root_directory, 'Logs')
config_directory: str = os.path.join(root_directory, 'Program Files', 'config')
user_directory: str = os.path.join(root_directory, 'User Profiles')

default_config: str = r'https://raw.githubusercontent.com/TheKliko/roblox-modloader/main/Program%20Files/config/config.json'


def system_not_supported() -> None:
    print(f'This program is not supported on {platform.system()}.')
    input('press ENTER to exit')

def get_launch_arguments() -> str:
    try:
        launch_argument: str = str(sys.argv[1][1:])
    except:
        launch_argument = 'None'
    return launch_argument.lower()

def run_launcher_process() -> None:
    from modules import launcher_process
    launcher_process.start()

def run_setup_process() -> None:
    from modules import setup_process
    setup_process.start()

def run_info_process() -> None:
    from modules import info_process
    info_process.start()

def main() -> None:
    try:
        if not platform.system() == 'Windows':
            system_not_supported()
            return None
        from modules import initialization
        initialization.start()

        launch_arguments = get_launch_arguments()
        if launch_arguments == 'launcher':
            run_launcher_process()
        elif launch_arguments == 'menu':
            run_setup_process()
        elif launch_arguments == 'info':
            run_info_process()
        else:
            logging.warning(f'Invalid launch argument(s): {launch_arguments}')
        from modules import termination
        termination.start()

    except Exception as e:
        from modules import user_interface as interface
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
        interface.print_message(f'An unexpected {type(e).__name__} occured: {str(e)}')
        interface.press_enter_to(message='exit')
    return None

if __name__ == '__main__':
    main()