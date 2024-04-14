import os
import sys
import logging

from modules import variables
from modules import termination
from modules import user_interface as interface
from modules.json_handler import get_json_value_from_input, update_json

from main import root_directory, config_directory

def start() -> None:
    logging.debug(f'Starting {os.path.splitext(os.path.basename(__file__))[0]}')

    config = variables.get(name='config_json')
    mods_directory: str = variables.get('mods_directory')
    
    project_name: str = get_json_value_from_input(config=config, key='title')
    project_author: str = get_json_value_from_input(config=config, key='author')
    modloader_version: str = get_json_value_from_input(config=config, key='version')
    roblox_version: str = get_json_value_from_input(config=config, key='installed_roblox_version')
    selected_mod_profile: str = get_json_value_from_input(config=config, key='selected_mod_profile')
    selected_fastflag_profile: str = get_json_value_from_input(config=config, key='selected_fastflag_profile')
    
    project_links = get_json_value_from_input(config=config, key='links')

    interface.open()

    interface.print_message(message=f'Project name: {project_name}')
    interface.print_message(message=f'Project author: {project_author}', spacing=0)
    interface.print_message(message=f'Project version: {modloader_version}', spacing=0)
    
    interface.print_message(message=f'Roblox Version: {roblox_version}')
    interface.print_message(message=f'Selected Mod Profile: {selected_mod_profile}', spacing=0)
    if selected_mod_profile:
        for mod in os.listdir(os.path.join(mods_directory, selected_mod_profile)):
            interface.print_message(message=f'  -> {mod}', spacing=0)
    interface.print_message(message=f'Selected FastFlag Profile: {selected_fastflag_profile}', spacing=0)

    interface.print_message('Useful links:')
    for name, link in project_links.items():
        interface.print_message(message=f'  -> {name}: {link}', spacing=0)

    interface.press_enter_to(message='exit')

    logging.debug(f'Finished {os.path.splitext(os.path.basename(__file__))[0]}')
    termination.start(timer=0)



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()