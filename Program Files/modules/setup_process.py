import os
import logging
import time

from modules import user_interface as interface
from modules import variables
from modules import termination

from modules.json_handler import get_json_value_from_input, get_json_complete, update_json_complete
from modules.roblox_update_handler import uninstall_roblox
from modules import rich_presence

from main import root_directory, config_directory


def start() -> None:
    logging.debug(f'Starting {os.path.splitext(os.path.basename(__file__))[0]}')

    sections: list[str] = ['save & exit', 'change mod profile', 'configure fastflags', 'reinstall roblox','help','settings']

    config: dict = variables.get(name='config_json')
    variables.set(name='config_new', value=config)

    variables.set(name='rich_presence_details', value='Modloader menu')
    variables.set(name='rich_presence_timestamp', value=int(time.time()))
    rich_presence.start()
    while True:
        interface.clear_console()
        interface.open(section='Setup')
        response_index, response_value = interface.selection_prompt(
            prompt='Select an option',
            options=sections,
            title=True
        )
        if 'exit' in response_value.lower():
            if exit_section():
                save_changes()
                termination.start(timer=1)
        elif 'mod' in response_value.lower():
            mods_section()
        elif 'fastflag' in response_value.lower():
            fastflags_section()
        elif 'reinstall' in response_value.lower():
            reinstall_section()
        elif 'help' in response_value.lower():
            help_section()
        elif 'setting' in response_value.lower():
            settings_section()


def exit_section() -> bool:
    interface.clear_console()
    interface.open(section='Save & Exit')
    if interface.confirmation_prompt(prompt='Save all changes and exit program?'):
        logging.info('Saving changes...')
        logging.debug(f'Finished {os.path.splitext(os.path.basename(__file__))[0]}')
        return True
    interface.clear_console()
    return False


def mods_section() -> None:
    user_directories: str = get_json_value_from_input(
        config=variables.get('config_new'),
        key='user_directories'
    )
    mods_directory: str = get_json_value_from_input(
        config=user_directories,
        key='mods_directory'
    )
    selected_indicator: str = '  <- [SELECTED]'
    
    while True:
        selected_mod_profile: str = get_json_value_from_input(
            config=variables.get('config_new'),
            key='selected_mod_profile'
        )

        sections: list[str] = ['Go Back']
        for mod_profile in os.listdir(os.path.join(root_directory, mods_directory)):
            if mod_profile == selected_mod_profile and not mod_profile == 'Default':
                mod_profile = f'{mod_profile}{selected_indicator}'
                sections.append(mod_profile)
            elif mod_profile == 'Default' and mod_profile == selected_mod_profile:
                mod_profile = f'{mod_profile}{selected_indicator}'
                sections.insert(1, mod_profile)
            elif mod_profile == 'Default':
                sections.insert(1, mod_profile)
            else:
                sections.append(mod_profile)
        
        add_none_section: bool = True
        if not selected_mod_profile:
            mod_profile = f'None{selected_indicator}'
            sections.append(mod_profile)
            add_none_section = False
        if add_none_section:
            sections.append('None')

        interface.clear_console()
        interface.open(section='Mod Profiles')
        response_index, response_value = interface.selection_prompt(
            prompt='Select a Mod Profile',
            options=sections
        )
        if 'back' in response_value.lower() or 'return' in response_value.lower():
            return None
        else:
            config: dict = variables.get('config_new')
            if 'none' in response_value.lower():
                config['selected_mod_profile'] = None
            else:
                config['selected_mod_profile'] = response_value
            variables.set(name='config_new', value=config)
        time.sleep(0.5)


def fastflags_section() -> None:
    fastflag_profiles: dict = get_json_complete(
        path=os.path.join(config_directory, 'fastflag_profiles.json'),
    )
    selected_indicator: str = '  <- [SELECTED]'

    while True:
        selected_fastflag_profile: str = get_json_value_from_input(
            config=variables.get('config_new'),
            key='selected_fastflag_profile'
        )

        sections: list[str] = ['Go Back']
        for fastflag_profile, fastflags_in_profile in fastflag_profiles.items():
            if fastflag_profile == selected_fastflag_profile:
                fastflag_profile = f'{fastflag_profile}{selected_indicator}'
                sections.append(fastflag_profile)
            else:
                sections.append(fastflag_profile)

        add_none_section: bool = True
        if not selected_fastflag_profile:
            fastflag_profile = f'None{selected_indicator}'
            sections.append(fastflag_profile)
            add_none_section = False
        if add_none_section:
            sections.append('None')

        interface.clear_console()
        interface.open(section='FastFlags')
        response_index, response_value = interface.selection_prompt(
            prompt='Select a FastFlag Profile',
            options=sections
        )

        if 'back' in response_value.lower() or 'return' in response_value.lower():
            return None
        else:
            config: dict = variables.get('config_new')
            if 'none' in response_value.lower():
                config['selected_fastflag_profile'] = None
            else:
                config['selected_fastflag_profile'] = response_value
            variables.set(name='config_new', value=config)
        time.sleep(0.5)


def reinstall_section() -> None:
    interface.clear_console()
    interface.open(section='Reinstall Roblox')
    if interface.confirmation_prompt(prompt='Do you wish to reinstall Roblox?'):
        uninstall_roblox()
        config = variables.get('config_new')
        config['installed_roblox_version'] = None
        variables.set(name='config_new', value=config)
        interface.print_message(message='Version folder removed!')
        interface.print_message(message='Roblox will be installed on next launch', spacing=0)
    interface.press_enter_to(message='return')
    return None


def help_section() -> None:
    links = get_json_value_from_input(
        config=variables.get('config_new'),
        key='links'
    )

    interface.clear_console()
    interface.open(section='Help')
    interface.print_message(message='If you need any help, please visit one of the links below')
    for name, link in links.items():
        interface.print_message(message=f'{name}: {link}', spacing=0)
    interface.press_enter_to(message='return')
    return None


def settings_section() -> None:
    sections: list[str] = ['Go back', 'Launch Roblox after setup']

    while True:
        interface.clear_console()
        interface.open(section='Settings')
        response_index, response_value = interface.selection_prompt(
            prompt='Select an option',
            options=sections
        )
        if 'back' in response_value.lower() or 'return' in response_value.lower():
            return None
        elif 'launch' in response_value.lower():
            settings_launch_roblox_section()

def settings_launch_roblox_section() -> None:
    config = variables.get('config_new')

    if interface.confirmation_prompt(
            prompt='Launch Roblox after exiting the setup process?',
            message=f'Current value: {config['launch_roblox_after_setup']}'
        ):
        config['launch_roblox_after_setup'] = True
    else:
        config['launch_roblox_after_setup'] = False
    variables.set(name='config_new', value=config)
    time.sleep(0.5)
    
    return None


def save_changes() -> None:
    logging.info('Saving changes...')
    config: dict = variables.get(name='config_new')
    config_old: dict = variables.get(name='config_json')

    if not config['selected_mod_profile'] == config_old['selected_mod_profile']:
        logging.info('Uninstalling Roblox because user selected a new mod profile')
        uninstall_roblox()

    try:
        update_json_complete(
            path=os.path.join(config_directory, 'config.json'),
            config=config
        )

    except Exception as e:
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')
    
    if get_json_value_from_input(
            config=config,
            key='launch_roblox_after_setup'
        ):
        variables.set(name='config_json', value=config)
        from modules import launcher_process
        launcher_process.start()

    return None



def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')

if __name__ == '__main__':
    main()