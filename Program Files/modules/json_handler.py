import os
import logging
import json


from main import config_directory, default_config

from modules.request_handler import request_json


def get_json_value_from_file(path: str, key: str) -> str | list | dict | int | float | bool | None:
    try:
        with open(path) as file:
            config = json.load(file)
            file.close()
        value = config[key]
        return value

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def get_json_value_from_input(config: dict, key: str) -> str | list | dict | int | float | bool | None:
    try:
        value = config[key]
        return value

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def get_json_complete(path: str) -> str | list | dict | int | float | bool | None:
    try:
        with open(path) as file:
            config = json.load(file)
            file.close()
        return config

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def update_json(
        path: str,
        key: str,
        value: str | list | dict | int | float | bool | None
    ) -> None:
    try:
        with open(path, 'r') as file:
            config = json.load(file)
            file.close()
        config[key] = value
        with open(path, 'w') as file:
            file.write(json.dumps(config, indent=4))

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    return None

def load_default_config() -> str | list | dict | int | float | bool | None:
    logging.info(f'loading default config...')
    try:
        config: dict = request_json(source=default_config)
        with open(os.path.join(config_directory, 'config.json'), 'w') as file:
            file.write(json.dumps(config, indent=4))
            file.close()
        return config

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