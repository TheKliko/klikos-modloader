import json
import logging
import os

from modules.interface import Print, Color
from modules.utils import variables


def load() -> None:
    logging.info('Loading settings . . .')
    Print('Loading settings . . .', color=Color.INITALIZE)

    root: str = variables.get('root')
    config_directory: str = os.path.join(root, 'Program Files', 'config')

    settings_filepath: str = os.path.join(config_directory, 'settings.json')
    with open(settings_filepath, 'r') as file:
        settings: dict = json.load(file)
        file.close()
    for key, value in settings.items():
        variables.set(key, value)

    integrations_filepath: str = os.path.join(config_directory, 'integrations.json')
    with open(integrations_filepath, 'r') as file:
        integrations: dict = json.load(file)
        file.close()
    for key, value in integrations.items():
        variables.set(key, value)