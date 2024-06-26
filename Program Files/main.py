import logging
import os
import platform
import sys
import threading
import time
import webbrowser

ROOT_DIRECTORY: str = os.path.dirname(os.path.dirname(__file__))
PROGRAM_FILES_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, 'Program Files')
sys.path.append(PROGRAM_FILES_DIRECTORY)
sys.path.append(os.path.join(PROGRAM_FILES_DIRECTORY, 'libs'))

from modules.presence import presence
from modules.processes import launcher
from modules.processes import launcher_studio
from modules.processes import menu
from modules.utils import interface
from modules.processes import shutdown
from modules.processes import startup
from modules.utils import variables

from modules.processes.startup import ConfigNotFoundError
from modules.utils.updater import UpdateAvailableError
from modules.roblox.updater import RobloxOutdatedError
from modules.roblox.updater_studio import StudioOutdatedError


CONFIG_DIRECTORY: str = os.path.join(PROGRAM_FILES_DIRECTORY, 'config')
MOD_PROFILES_FILEPATH: str = os.path.join(CONFIG_DIRECTORY, 'mod_profiles.json')
FASTFLAG_PROFILES_FILEPATH: str = os.path.join(CONFIG_DIRECTORY, 'fastflag_profiles.json')
LATEST_RELEASE_URL: str = r'https://github.com/TheKliko/klikos-modloader/releases/latest'
LOGGING_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, 'Logs')
LOGGING_FILENAME: str = f'log_{time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())}.log'
LOGGING_FILEPATH: str = os.path.join(LOGGING_DIRECTORY, LOGGING_FILENAME)
OPERATING_SYSTEM: str = platform.system()
SETTINGS_FALLBACK: str = r'https://raw.githubusercontent.com/TheKliko/roblox-modloader/main/Program%20Files/config/settings.json'
SETTINGS_FILEPATH: str = os.path.join(CONFIG_DIRECTORY, 'settings.json')
SUPPORTED_PLATFORMS: list[str] = ['Windows']


class LaunchArgumentError(Exception):
    """Exception raised when attempting to launch the program with invalid launch arguments"""
    pass


def main() -> None:
    try:
        # Startup process
        initialize()
        startup.start()

        # Discord RPC
        threading.Thread(target=presence.start, daemon=True).start()

        # Main process
        launch_main_program()

        # Shutdown process
        shutdown.start()
    
    # Error handling
    except SystemError as e:  # User tries to run this program on an unsupported platform
        interface.clear()
        interface.text(f'A {type(e).__name__} occured: {e}')
        interface.text(
            [
                'Currently, this program is only available for Windows.',
                'Try running it on a Windows PC instead.'
            ]
        )
    
    except ConfigNotFoundError as e:  # Settings or version info config file could not be found
        interface.open(section='An error occured!')
        logging.error(f'A {type(e).__name__} occured: {e}')
        interface.text(f'A {type(e).__name__} occured: {e}', spacing=0)
        interface.text(
            [
                'Try reinstalling the program.',
                'If that doesn\'t fix this issue, please join our discord server and ask for help.'
            ]
        )
    
    except UpdateAvailableError as e:  # An update to this program is available
        interface.open(section='An update is available!')
        interface.text(
            [
                f'{e}',
                'The URL to the latest version will now open in your default browser.'
            ]
        )
        variables.set(name='exception_code_bypass', value=True)
        variables.set(name='rpc_state', value='error')
        variables.set(name='error_type', value=type(e).__name__)

        print()
        input('Press enter to continue . . .')
        webbrowser.open(LATEST_RELEASE_URL, new=2)

    except RobloxOutdatedError as e:  # User refused to install a Roblox update
        interface.open(section='An error occured!')
        interface.text(
            [
                f'A {type(e).__name__} occured: {e}',
                'This is a standard exception caused by choosing not to update Roblox.',
                'To fix this, choose to accept when prompted to update Roblox.'
            ]
        )
        variables.set(name='error_type', value=type(e).__name__)

    except StudioOutdatedError as e:  # User refused to install a Roblox Studio update
        interface.open(section='An error occured!')
        interface.text(
            [
                f'A {type(e).__name__} occured: {e}',
                'This is a standard exception caused by choosing not to update Roblox Studio.',
                'To fix this, choose to accept when prompted to update Roblox Studio.'
            ]
        )
        variables.set(name='error_type', value=type(e).__name__)
    
    except LaunchArgumentError as e:  # User tried to launch program with invalid launch arguments
        interface.open(section='An error occured!')
        interface.text(f'A {type(e).__name__} occured: {e}')
        variables.set(name='error_type', value=type(e).__name__)
    
    except ImportError as e:  # Required module or library is missing
        interface.open(section='An error occured!')
        interface.text([
            f'An {type(e).__name__} occured: {e}',
            '',
            'This error means that a required library was not included with this program.',
            'Please report this issue in the discord server or manually install the required library.'
        ])
        variables.set(name='error_type', value=type(e).__name__)
    
    except NotImplementedError as e:  # User runs a version of this program that was not finished
        interface.open(section='An error occured!')
        interface.text(
            [
                f'A {type(e).__name__} occured: {e}',
                '',
                'You appear to be using an incomplete version of this program.',
                'Please report this issue in the discord server.'
            ]
        )
        variables.set(name='error_type', value=type(e).__name__)

    except Exception as e:  # Unknown errors / Other errors
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
        interface.open(section='An error occured!')
        interface.text(f'An unexpected {type(e).__name__} occured: {str(e)}', spacing=0)
        variables.set(name='error_type', value=type(e).__name__)
    
    # The following code executes only if an exception occured.
    if not variables.get_silent('exception_code_bypass'):
        variables.set(name='rpc_state', value='error')
        USEFUL_LINKS: dict = variables.get('links')
        interface.text(f'Please visit one of the following links if you need any further assistance:', spacing=2)
        interface.text(
            [
                f'\u2022 {name}: {url}' for name, url in USEFUL_LINKS.items()
            ],
            spacing=0
        )
        print()
        input('Press ENTER to exit . . .')
    shutdown.start()

    return None


def initialize() -> None:
    print('Initializing...')

    if OPERATING_SYSTEM not in SUPPORTED_PLATFORMS:
        raise SystemError(f'Unsupported OS \'{OPERATING_SYSTEM}\' detected.')
    
    initialize_logger()

    variables.set(name='root_directory', value=ROOT_DIRECTORY)
    variables.set(name='program_files_directory', value=PROGRAM_FILES_DIRECTORY)
    variables.set(name='config_directory', value=CONFIG_DIRECTORY)
    variables.set(name='mod_profiles_filepath', value=MOD_PROFILES_FILEPATH)
    variables.set(name='fastflag_profiles_filepath', value=FASTFLAG_PROFILES_FILEPATH)
    variables.set(name='logging_directory', value=LOGGING_DIRECTORY)
    variables.set(name='logging_filepath', value=LOGGING_FILEPATH)
    variables.set(name='settings_fallback', value=SETTINGS_FALLBACK)
    variables.set(name='settings_filepath', value=SETTINGS_FILEPATH)


def initialize_logger() -> None:
    if not os.path.isdir(LOGGING_DIRECTORY):
        os.makedirs(name=LOGGING_DIRECTORY, exist_ok=True)

    elif os.path.isfile(LOGGING_FILEPATH):
        os.remove(path=LOGGING_FILEPATH)

    logging.basicConfig(
    format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(funcName)s] [line_%(lineno)d]: %(message)s',
    datefmt='%Y-%m-%d_%H:%M:%S',
    filename=LOGGING_FILEPATH,
    encoding='utf-8',
    level=logging.DEBUG
    )

    logging.info(f'Writing logs to: {LOGGING_FILENAME}')
    return None


def launch_main_program() -> None:
    LAUNCH_ARGUMENTS: str = get_launch_arguments()

    if LAUNCH_ARGUMENTS == '-launcher':
        launcher.start()

    elif LAUNCH_ARGUMENTS == '-studio':
        launcher_studio.start()

    elif LAUNCH_ARGUMENTS == '-menu':
        menu.start()
    
    elif LAUNCH_ARGUMENTS.startswith('roblox-player'):
        variables.set(name='active_launch_arguments', value=LAUNCH_ARGUMENTS)
        launcher.start()

    else:
        raise LaunchArgumentError(f'Invalid launch argument(s): {LAUNCH_ARGUMENTS}')


def get_launch_arguments() -> str:
    try:
        launch_argument = str(sys.argv[1])
    
    except:
        launch_argument = f'-{variables.get('default_launch_arguments')}'
    
    return launch_argument.lower()


if __name__ == '__main__':
    main()