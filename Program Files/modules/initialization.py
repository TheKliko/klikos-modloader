import os
import logging
import time
import glob

from main import root_directory, logging_directory, config_directory

from modules.json_handler import (
    get_json_complete,
    load_default_config,
    get_json_value_from_file,
    get_json_value_from_input,
    update_json
)
from modules.directory_functions import create_directory
from modules import variables


def start() -> None:
    if not os.path.isdir(logging_directory):
        os.makedirs(logging_directory, exist_ok=True)
    logging_filename: str = initialize_logger()

    variables.create_file()
    variables.set(name='logging_filename', value=logging_filename)

    config_json = get_json_complete(path=os.path.join(config_directory, 'config.json'))
    if not config_json:
        config_json = load_default_config()
    current_version = get_json_value_from_file(path=os.path.join(config_directory, 'version_info.json'), key='version')
    if not current_version:
        current_version = 'UNKNOWN_VERSION'
    config_json['version'] = current_version
    variables.set(name='config_json', value=config_json)
    variables.set(name='rich_presence_game_id', value='not_in_game')
    variables.set(name='in_game', value=False)
    variables.set(name='in_menu', value=False)

    # Change terminal title using https://stackoverflow.com/a/10229529
    title: str = get_json_value_from_input(config=config_json, key='title')
    os.system('title ' + title)

    max_log_files = get_json_value_from_file(path=os.path.join(config_directory, 'config.json'), key='max_log_files') or 20
    clear_old_logs(max_log_files=max_log_files)

    user_directories = get_json_value_from_file(
        path=os.path.join(config_directory, 'config.json'),
        key='user_directories'
    )
    variables.set(name='user_directories', value=user_directories)
    create_user_directories()

    version_directory: str = variables.get(name='version_directory')
    installed_roblox_version = get_json_value_from_input(config=config_json, key='installed_roblox_version')
    if not installed_roblox_version:
        pass
    elif not os.path.isdir(os.path.join(version_directory, installed_roblox_version)):
        installed_roblox_version = 'none'
        update_json(
            path=os.path.join(config_directory, 'config.json'),
            key='installed_roblox_version',
            value=None
        )
        config_json['installed_roblox_version'] = 'none'
        variables.set(name='config_json', value=config_json)

    logging.debug('Finished initialization')
    return None



def initialize_logger() -> str:
    logging_filename: str = f'log_{time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())}.log'
    logging.basicConfig(
    format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(funcName)s] [line_%(lineno)d]: %(message)s',
    datefmt='%Y-%m-%d_%H:%M:%S',
    filename=os.path.join(logging_directory, logging_filename),
    encoding='utf-8',
    level=logging.DEBUG
    )
    logging.info(f'Writing logs to: {logging_filename}')
    return logging_filename

def clear_old_logs(max_log_files: int) -> None:
    log_files = sorted(glob.glob(os.path.join(logging_directory, "*.log")), key=os.path.getctime)
    if len(log_files) > max_log_files:
        num_files_to_delete = len(log_files) - max_log_files
        for i in range(num_files_to_delete):
            oldest_log_file = log_files[i]
            oldest_log_filename = os.path.basename(oldest_log_file)
            os.remove(oldest_log_file)
            logging.info(f'Removed old log file: {oldest_log_filename}')

def create_user_directories() -> None:
    user_directories = get_json_value_from_input(config=variables.get('config_json'), key='user_directories')

    version_directory = os.path.join(root_directory, user_directories['version_directory'])
    mods_directory = os.path.join(root_directory, user_directories['mods_directory'])

    variables.set(name='version_directory', value=version_directory)
    variables.set(name='mods_directory', value=mods_directory)

    try:
        for directory_name, directory_path in user_directories.items():
            if not os.path.exists(directory_path):
                create_directory(path=root_directory, name=directory_path)

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()