import os
import logging
import multiprocessing
import subprocess
import time

from modules import variables
from modules import user_interface as interface
from modules.directory_functions import copy_directory
from modules.json_handler import update_json, get_json_value_from_input
from modules.request_handler import request_json

from main import config_directory
version_directory: str = variables.get(name='version_directory')
roblox_install_location: str = os.path.join(str(os.getenv('LOCALAPPDATA')), 'Roblox', 'Versions')


def check_for_update() -> None:
    logging.info('Checking for Roblox update...')
    try:
        latest_roblox_version = get_latest_roblox_version()
        variables.set(name='latest_roblox_version', value=latest_roblox_version)

        if not os.path.exists(os.path.join(version_directory, latest_roblox_version)):
            interface.print_message(message=f'A new Roblox version is available:')
            interface.print_message(message=f'{latest_roblox_version}', spacing=0)
            if not interface.confirmation_prompt(prompt='Do you wish to install?'):
                variables.set(name='using_latest_version', value=False)
                return None
            
            update_roblox(latest_roblox_version=latest_roblox_version)

            copy_directory(
                source = os.path.join(roblox_install_location, latest_roblox_version),
                destination = os.path.join(version_directory, latest_roblox_version)
            )
        variables.set(name='using_latest_version', value=True)

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')

def update_roblox(latest_roblox_version: str) -> None:
    logging.info('Updating Roblox...')
    process_1 = multiprocessing.Process(target=run_roblox_installer, args='')
    process_2 = multiprocessing.Process(target=exit_roblox_installer, args='')
    process_1.start()
    process_2.start()
    process_2.join()
    update_json(
        path=os.path.join(config_directory, 'config.json'),
        key='installed_roblox_version',
        value=latest_roblox_version
    )

def run_roblox_installer() -> None:
    command: str = f'"{os.path.join('Program Files', 'RobloxPlayerInstaller.exe')}"'
    subprocess.run(command)

def exit_roblox_installer() -> None:
    while True:
        if process_exists('RobloxPlayerbeta.exe'):
            taskkill_roblox_player_beta = 'taskkill /f /im RobloxPlayerBeta.exe'
            taskkill_roblox_player_installer = 'taskkill /f /im RobloxPlayerInstaller.exe'
            subprocess.run(taskkill_roblox_player_beta, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(taskkill_roblox_player_installer, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return
        time.sleep(0.5)

def get_latest_roblox_version() -> str:
    config: dict = request_json(source=r'https://clientsettingscdn.roblox.com/v2/client-version/windowsplayer')
    value: str = get_json_value_from_input(config=config, key='clientVersionUpload')
    return value

# Check if process exists using https://stackoverflow.com/a/29275361
def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())



def main():
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()