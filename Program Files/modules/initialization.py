import os
import logging
import time
import glob

from main import root_directory, logging_directory, config_directory, default_config, user_directory

from modules.json_handler import get_json_complete, load_default_config, get_json_value_from_file



def initialize() -> None:
    initialize_logger()

    global config_json
    config_json = get_json_complete(path=os.path.join(config_directory, 'config.json'))
    if not config_json:
        config_json = load_default_config()

    max_log_files = get_json_value_from_file(path=os.path.join(config_directory, 'config.json'), key='max_log_files') or 20
    clear_old_logs(max_log_files=max_log_files)

    global required_directories
    required_directories = get_json_value_from_file(path=os.path.join(config_directory, 'config.json'), key='user_directories')
    load_user_directories()



def initialize_logger() -> None:
    logging_filename: str = f'log_{time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())}.log'
    logging.basicConfig(
    format='%(asctime)s [%(levelname)s] [%(filename)s:%(funcName)s] [line_%(lineno)d]: %(message)s',
    datefmt='%Y-%m-%d_%H:%M:%S',
    filename=os.path.join(logging_directory, logging_filename),
    encoding='utf-8',
    level=logging.DEBUG
    )
    logging.info(f'Writing logs to: {logging_filename}')

def clear_old_logs(max_log_files: int) -> None:
    log_files = sorted(glob.glob(os.path.join(logging_directory, "*.log")), key=os.path.getctime)
    if len(log_files) > max_log_files:
        num_files_to_delete = len(log_files) - max_log_files
        for i in range(num_files_to_delete):
            oldest_log_file = log_files[i]
            oldest_log_filename = os.path.basename(oldest_log_file)
            os.remove(oldest_log_file)
            logging.info(f'Removed old log file: {oldest_log_filename}')

def load_user_directories() -> None:
    global version_directory, mods_directory, fastflags_directory
    version_directory = os.path.join(root_directory, required_directories['version_directory'])
    mods_directory = os.path.join(user_directory, required_directories['mods_directory'])
    fastflags_directory = os.path.join(user_directory, required_directories['fastflags_directory'])
    try:
        for directory in version_directory, mods_directory, fastflags_directory:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logging.info(f'Created directory: {directory}')
    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None



def main():
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()