import glob
import logging
import os

from modules.utils import filesystem
from modules.utils import json_manager
from modules.utils import updater
from modules.utils import variables


def run() -> None:
    """Begin the startup process"""

    logging.info('Begin startup process')

    check_core_files()
    set_variables()
    clear_old_logs()
    check_user_directories()
    variables_cleanup()

    # Change terminal title using https://stackoverflow.com/a/10229529
    os.system(f'title {variables.get('project_data')['name']}')

    updater.check()

    logging.info('End startup process')


def check_core_files() -> None:
    """Check if required files exist"""

    DIRECTORIES: list[str] = [
        variables.get('config_directory')
    ]
    FILES: list[str] = [
        variables.get('settings_filepath'),
        variables.get('mod_profiles_filepath'),
        variables.get('fastflag_profiles_filepath')
    ]

    filesystem.validate(
        {
            'files': FILES,
            'directories': DIRECTORIES
        }
    )


def set_variables() -> None:
    SETTINGS: str = variables.get('settings_filepath')
    CONFIG: dict = json_manager.read(SETTINGS)

    for key, value in CONFIG.items():
        variables.set(key, value)


def clear_old_logs() -> None:
    logging.info('Clearing old logs')

    LOGGING_DIRECTORY: str = variables.get('logging_directory')
    USER_SETTINGS: dict = variables.get('user_settings')
    MAX_LOG_FILES: int = USER_SETTINGS['max_log_files']['value']
    LOGS: list = sorted(glob.glob(os.path.join(LOGGING_DIRECTORY, "*.log")), key=os.path.getctime, reverse=True)

    if len(LOGS) <= MAX_LOG_FILES:
        logging.info('No logs cleared')
        return
    
    OLD_LOGS: list[str] = LOGS[MAX_LOG_FILES:]
    for log in OLD_LOGS:
        try:
            os.remove(log)
            logging.info(f'Removed old log: {os.path.basename(log)}')

        except PermissionError as e:
            logging.warning(f'[{type(e).__name__}] Failed to remove log: {os.path.basename(log)}')
        
        except FileNotFoundError as e:
            pass


def check_user_directories() -> None:
    ROOT: str = variables.get('root')
    USER_DIRECTORIES: dict = variables.get('user_directories')
    for key, value in USER_DIRECTORIES.items():
        directory: str = str(value).replace(r'{ROOT}', ROOT)
        filesystem.validate(
            directory,
            mode=filesystem.ValidationMode.DIRECTORY,
            create_missing_directories=True
        )
        variables.set(f'{key}_directory', directory)


def variables_cleanup() -> None:
    USER_SETTINGS: dict = variables.get('user_settings')
    DISCORD_RPC: bool = USER_SETTINGS['discord_rpc']['value']
    variables.set('discord_rpc', DISCORD_RPC)

    variables.remove('user_directories')
    variables.remove('user_settings')
    variables.remove('licenses')


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()