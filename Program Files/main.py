import logging
import os
import platform
import sys
import threading
import time

ROOT: str = os.path.dirname(os.path.dirname(__file__))
PROGRAM_FILES: str = os.path.dirname(__file__)
sys.path.append(os.path.join(PROGRAM_FILES, 'libraries'))
sys.path.append(PROGRAM_FILES)

from modules import interface
from modules.presence import rpc
from modules.processes import startup
from modules.processes import menu
from modules.processes import launcher
from modules.processes import shutdown
from modules.utils import variables
from modules.utils.filesystem import ValidationError


BULLET: str = '\u2022'

LOGGING_DIRECTORY: str = os.path.join(ROOT, 'Logs')
CONFIG_DIRECTORY: str = os.path.join(PROGRAM_FILES, 'config')
MOD_PROFILES_FILEPATH: str = os.path.join(CONFIG_DIRECTORY, 'mod_profiles.json')
FASTFLAG_PROFILES_FILEPATH: str = os.path.join(CONFIG_DIRECTORY, 'fastflag_profiles.json')
SETTINGS_FILEPATH: str = os.path.join(CONFIG_DIRECTORY, 'settings.json')

OPERATING_SYSTEM: str = platform.system()
SUPPORTED_PLATFORMS: list[str] = ['Windows']

DISCORD_FALLBACK: str = r'https://discord.gg/nEjUwdSP9P'
WEBSITE_FALLBACK: str = r'https://thekliko.github.io/klikos-modloader'
GITHUB_FALLBACK: str = r'https://github.com/TheKliko/klikos-modloader'
LATEST_RELEASE_FALLBACK: str = r'https://github.com/TheKliko/klikos-modloader/releases/latest'


class PlatformError(Exception):
    """Exception raised when attempting to launch the program on an unsupported platform"""
    pass


def main() -> None:
    EXCEPTION_BYPASS = False

    try:
        # Startup process
        initialize()
        startup.run()
        
        # Discord rich presence
        presence = threading.Thread(target=rpc.connect, name='rich-presence', daemon=True)
        presence.start()

        # Main process
        LAUNCH_MODE = get_launch_args()

        if LAUNCH_MODE in ['launcher', 'roblox', 'play', 'launch', 'l', 'p', 'r']:  # Don't know why I even bother accepting more than 1 argument for the same launch mode
            launcher.run('roblox')

        elif LAUNCH_MODE in ['studio', 'create', 'roblox-studio', 'play-studio' , 'launch-studio', 'launcher-studio', 's', 'ls', 'ps', 'rs']:
            launcher.run('studio')

        else:
            menu.run()

        # Shutdown process
        shutdown.run()
        sys.exit()


    # Error handling
    except PlatformError as e:  # User tries to run this program on an unsupported platform
        logging.error(f'[{type(e).__name__}] {e}')
        variables.set('rpc_status', rpc.RichPresenceStatus.ERROR)
        variables.set('rpc_details', f'A {type(e).__name__} occured')
        variables.set('rpc_state', str(e))

        interface.clear()
        interface.open(
            [
                f'A {type(e).__name__} occured',
                f'{e}'
            ]
        )
        interface.text(
            ['Currently, this program is only available on the following platforms:']
            + [f'{BULLET} {platform}' for platform in SUPPORTED_PLATFORMS]
        )
        interface.newline()

    except NotImplementedError as e:  # User is running an unfinished version
        logging.error(f'[{type(e).__name__}] {e}')
        variables.set('rpc_status', rpc.RichPresenceStatus.ERROR)
        variables.set('rpc_details', f'A {type(e).__name__} occured')
        variables.set('rpc_state', str(e))
        
        variables.set('exit_installer_loop', True)
        
        interface.clear()
        interface.open(
            [
                f'An {type(e).__name__} occured',
                f'{e}'
            ]
        )

        try:
            TROUBLESHOOTING_URLS: dict = variables.get('troubleshooting_urls', silent=False)
            DISCORD: str = TROUBLESHOOTING_URLS['discord']

        except:
            logging.warning('Using fallback troubleshooting URLs')
            DISCORD: str = DISCORD_FALLBACK

        interface.text(
            [
                'You shouldn\'t encounter this error.',
                '',
                'If you do, please report this in our Discord server:',
                f'{BULLET} {DISCORD}'
            ]
        )
        EXCEPTION_BYPASS = True

    except ValidationError as e:  # Required files are missing
        logging.error(f'[{type(e).__name__}] {e}')
        variables.set('rpc_status', rpc.RichPresenceStatus.ERROR)
        variables.set('rpc_details', f'A {type(e).__name__} occured')
        variables.set('rpc_state', str(e))

        interface.clear()
        interface.open(
            [
                f'An {type(e).__name__} occured',
                f'{e}'
            ]
        )

        try:
            TROUBLESHOOTING_URLS: dict = variables.get('troubleshooting_urls', silent=False)
            LATEST_RELEASE: str = TROUBLESHOOTING_URLS['latest_release']

        except:
            logging.warning('Using fallback troubleshooting URLs')
            LATEST_RELEASE: str = LATEST_RELEASE_FALLBACK

        interface.text(
            [
                'Core files are missing or corrupted, please reinstall this program:',
                f'{BULLET} {LATEST_RELEASE}'
            ]
        )
        interface.newline()


    except Exception as e:  # Other (unexpected) errors
        logging.error(f'[{type(e).__name__}] {e}')
        variables.set('rpc_status', rpc.RichPresenceStatus.ERROR)
        variables.set('rpc_details', f'A {type(e).__name__} occured')
        variables.set('rpc_state', str(e))
        
        variables.set('exit_installer_loop', True)
        
        interface.clear()
        interface.open(
            [
                f'An unexpected {type(e).__name__} occured',
                f'{e}'
            ]
        )
    
    
    if not EXCEPTION_BYPASS:
        try:
            TROUBLESHOOTING_URLS: dict = variables.get('troubleshooting_urls', silent=False)
            DISCORD: str = TROUBLESHOOTING_URLS['discord']
            WEBSITE: str = TROUBLESHOOTING_URLS['website']
            GITHUB: str = TROUBLESHOOTING_URLS['github']
            LATEST_RELEASE: str = TROUBLESHOOTING_URLS['latest_release']

        except:
            logging.warning('Using fallback troubleshooting URLs')
            DISCORD: str = DISCORD_FALLBACK
            WEBSITE: str = WEBSITE_FALLBACK
            GITHUB: str = GITHUB_FALLBACK
            LATEST_RELEASE: str = LATEST_RELEASE_FALLBACK

        interface.text(
            [
                'Please join our Discord server if you need any help:',
                f'{BULLET} {DISCORD}',
                '',
                'Or visit our website:',
                f'{BULLET} {WEBSITE}'
            ]
        )
    
    interface.divider()
    interface.prompt('Press ENTER to exit . . .')


def initialize() -> None:
    print('Initializing...')

    if OPERATING_SYSTEM not in SUPPORTED_PLATFORMS:
        raise OSError(f'Unsupported OS \'{OPERATING_SYSTEM}\' detected.')
    
    initialize_logger()
    set_variables()


def initialize_logger() -> None:
    LOGGING_FILENAME: str = f'log_{time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())}.log'
    LOGGING_FILEPATH: str = os.path.join(LOGGING_DIRECTORY, LOGGING_FILENAME)
    
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


def set_variables() -> None:
    variables.set('root', ROOT)
    variables.set('program_files_directory', PROGRAM_FILES)
    variables.set('logging_directory', LOGGING_DIRECTORY)
    variables.set('config_directory', CONFIG_DIRECTORY)
    variables.set('settings_filepath', SETTINGS_FILEPATH)
    variables.set('mod_profiles_filepath', MOD_PROFILES_FILEPATH)
    variables.set('fastflag_profiles_filepath', FASTFLAG_PROFILES_FILEPATH)


def get_launch_args() -> str:
    if len(sys.argv) > 1:
        return str(sys.argv[1]).lower().removeprefix('-').removeprefix('-')
    return None


if __name__ == '__main__':
    main()