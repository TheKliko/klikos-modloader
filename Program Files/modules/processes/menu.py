"""# menu.py

menu.py is a module used in Kliko's modloader,
it's purpose is to take care of the everything that happens when the program is launched with the "-menu" argument.
"""


import logging
import os
import re
import time
import webbrowser

from modules.utils import directory
from modules.utils import interface
from modules.utils import read_json
from modules.utils import variables
from modules.utils import write_json

from modules.utils.request_handler import request
from modules.roblox.updater import remove_version_directory


def start() -> None:
    """Function called to begin the menu process"""
    
    variables.set(name='rpc_state', value='menu')
    variables.set(name='rpc_timestamp', value=int(time.time()))

    SECTIONS: list[str] = ['Save & Exit', 'Choose Mod Profiles', 'Configure Mod Profiles', 'FastFlags', 'Settings', 'Help']

    while True:
        interface.open('Menu')

        index, response = interface.select(options=SECTIONS)

        if 'exit' in response.lower():
            interface.open('Save & Exit')
            if interface.confirm(prompt='Save changes and exit program?'):
                save_changes()
                time.sleep(0.15)
                break

        elif 'choose' in response.lower():
            mod_section_switch()

        elif 'configure' in response.lower():
            mod_section_configure()

        elif 'fastflags' in response.lower():
            fastflag_section()

        elif 'settings' in response.lower():
            settings_section()

        elif 'help' in response.lower():
            help_section()


def mod_section_switch() -> None:
    SELECTED_ITEM_INDICATOR: str = variables.get('selected_item_indicator')
    CONFIG_DIRECTORY: str = variables.get('config_directory')
    MOD_PROFILES: dict = read_json.complete(filepath=os.path.join(CONFIG_DIRECTORY, 'mod_profiles.json'))

    while True:
        CURRENT_MOD_PROFILE: str = variables.get('selected_mod_profile')

        interface.open('Select a mod profile')

        index, response = interface.select(
            ['Go Back']
            + [profile if not profile == CURRENT_MOD_PROFILE else f'{CURRENT_MOD_PROFILE}{SELECTED_ITEM_INDICATOR}' for profile, mods in MOD_PROFILES.items()]
            + ['None' if CURRENT_MOD_PROFILE is not None else f'None{SELECTED_ITEM_INDICATOR}'],
            prompt='Select a mod profile'
        )

        if response.lower() == 'go back':
            return None
        
        elif response.lower() == 'none':
            variables.set(name='selected_mod_profile', value=None)
            continue

        for profile, info in MOD_PROFILES.items():
            if response == profile:
                variables.set(name='selected_mod_profile', value=response)


def mod_section_configure() -> None:
    CONFIG_DIRECTORY: str = variables.get('config_directory')

    while True:
        mod_profiles: dict = read_json.complete(filepath=os.path.join(CONFIG_DIRECTORY, 'mod_profiles.json'))

        interface.open('Configure mod profiles')

        index, response = interface.select(
            ['Go Back'] + [profile for profile, mods in mod_profiles.items()] + ['Create New Profile'],
            prompt='Choose a mod profile'
        )

        if response.lower() == 'go back':
            return None
        
        elif response.lower() == 'create new profile':
            interface.open('Mod Profile Creation')
            profile_name: str = interface.prompt(
                ['Choose a name for your new mod profile'],
                restrict_responses=[profile for profile, mods in mod_profiles.items()]
            )
            write_json.value(filepath=os.path.join(CONFIG_DIRECTORY, 'mod_profiles.json'), key=profile_name, value={})
            logging.info(f'Created mod profile: {profile_name}')

        for profile, mods in mod_profiles.items():
            if response == profile:
                
                logging.info(f'Configuring mod profile: {response}')
                configure_mod_profile(response)


def configure_mod_profile(profile) -> None:
    SECTIONS: list[str] = ['Go Back', 'View Mods', 'Add Mods', 'Remove Mods', 'Change Mod Priorities', 'Rename Mod Profile', 'Delete Mod Profile']

    CONFIG_DIRECTORY: str = variables.get('config_directory')
    MOD_PROFILES_FILEPATH: str = os.path.join(CONFIG_DIRECTORY, 'mod_profiles.json')

    while True:
        interface.open(f'Mod profile: {profile}')

        index, response = interface.select(options=SECTIONS)

        if 'back' in response.lower() or 'return' in response.lower():
            return None

        elif 'view' in response.lower():  # View mods in profile
            MODS: dict = read_json.value(filepath=MOD_PROFILES_FILEPATH, key=profile)
            
            interface.open(f'Viewing mods in: {profile}')
            
            interface.text(
                [
                    'A lower number indicates a higher priority',
                    ''
                ]
                + [f'[priority: {priority}]: {mod}' if MODS.items() is not None else 'No mods found!' for priority, mod in sorted(MODS.items(), key=lambda x: int(x[0]))]
                + [
                    '',
                    ''
                ]
            )
            input('Press ENTER to return . . .')

        elif 'add' in response.lower():  # Add mods to profile
            while True:
                mods: dict = read_json.value(filepath=MOD_PROFILES_FILEPATH, key=profile)
                installed_mods: list = directory.subdirectories(path=variables.get('mod_directory'))

                interface.open(f'Add mods to: {profile}')

                index, response = interface.select(
                    ['Go Back']
                    + [mod for mod in installed_mods if not mod in mods.values()],
                    prompt=f'Select a mod to add to: {profile}'
                )

                if response.lower() == 'go back':
                    break

                default_priority: int = 1
                while str(default_priority) in mods:
                    default_priority += 1
                mods[str(default_priority)] = response

                new_mods: dict = {priority: mod for priority, mod in sorted(mods.items(), key=lambda x: int(x[0]))}

                write_json.value(filepath=MOD_PROFILES_FILEPATH, key=profile, value=new_mods)
                logging.info(f'Added mod {response} to {profile}')

        elif 'remove' in response.lower():  # Remove mods from profile
            while True:
                interface.open(f'Remove mods from: {profile}')

                mods: dict = read_json.value(filepath=MOD_PROFILES_FILEPATH, key=profile)

                index, response = interface.select(
                    ['Go Back']
                    + [mod for priority, mod in sorted(mods.items(), key=lambda x: int(x[0]))],
                    prompt=f'Select a mod to remove from: {profile}'
                )

                if response.lower() == 'go back':
                    break

                new_mods: dict = {priority: mod for priority, mod in sorted(mods.items(), key=lambda x: int(x[0])) if not mod == response}

                write_json.value(filepath=MOD_PROFILES_FILEPATH, key=profile, value=new_mods)
                logging.info(f'Removed mod {response} from {profile}')

        elif 'change' in response.lower():  # Edit mod priorities
            while True:

                mods: dict = read_json.value(filepath=MOD_PROFILES_FILEPATH, key=profile)
                mod_items = sorted(mods.items(), key=lambda x: int(x[0]))

                interface.open('Edit mod priority')

                interface.text(
                    [
                        'A lower number indicates a higher priority',
                        '(Mods get appled in order of priority [low -> high])'
                    ]
                )

                index, response = interface.select(
                        ['Go Back']
                        + [f'{mod} [priority: {priority}]' for priority, mod in sorted(mods.items(), key=lambda x: int(x[0]))],
                        prompt=f'Select a mod to change it\'s priority in: {profile}'
                    )
                
                pattern = r' \[priority: -?\d+\]'
                response = re.sub(pattern, '', response)

                if response.lower() == 'go back':
                    break

                current_priority: str = next(priority for priority, mod in mod_items if mod == response)
                new_priority = interface.select_number(prompt=f'Choose a new priority for {response} (current: {current_priority})')

                if int(current_priority) == new_priority:
                    pass

                elif not str(new_priority) in mods:
                    mods[str(new_priority)] = mods.pop(str(current_priority))
                
                else:  # User changes mod priority to the same priority of a different mod, different mod will be moved down until it can be placed.
                    default_priority: int = new_priority + 1
                    chosen_mod = mods.pop(str(current_priority))

                    while str(default_priority) in mods:
                        default_priority += 1

                    mods[str(default_priority)] = mods[str(new_priority)]
                    mods[str(new_priority)] = chosen_mod

                write_json.value(filepath=MOD_PROFILES_FILEPATH, key=profile, value=mods)
                logging.info(f'Changed priority of {response} in {profile}')
                time.sleep(0.15)

        elif 'rename' in response.lower():  # Rename mod profile
            SETTINGS_FILEPATH: str = variables.get('settings_filepath')
            mod_profiles: dict = read_json.complete(filepath=MOD_PROFILES_FILEPATH)

            interface.open(f'Rename mod profile: {profile}')

            new_profile_name: str = interface.prompt(
                ['Choose a new name for your mod profile'],
                restrict_responses=[profile for profile, mods in mod_profiles.items()]
            )
            write_json.rename_key(filepath=MOD_PROFILES_FILEPATH, key=profile, name=new_profile_name)

            if variables.get('selected_mod_profile') == profile:
                variables.set(name='selected_mod_profile', value=new_profile_name)
            
            if read_json.value(filepath=SETTINGS_FILEPATH, key='selected_mod_profile') == profile:
                write_json.value(filepath=SETTINGS_FILEPATH, key='selected_mod_profile', value=new_profile_name)

            logging.info(f'Renamed mod profile: {profile} -> {new_profile_name}')
            profile = new_profile_name

        elif 'delete' in response.lower():  # Delete mod profile
            SETTINGS_FILEPATH: str = variables.get('settings_filepath')

            interface.open(f'Delete mod profile {profile}')

            interface.text('CAUTION: This cannot be undone!')
            if interface.confirm(f'Are you sure you want to delete the following mod profile: {profile}'):
                write_json.remove_key(filepath=MOD_PROFILES_FILEPATH, key=profile)
                if read_json.value(filepath=SETTINGS_FILEPATH, key='selected_mod_profile') == profile:
                    write_json.value(filepath=SETTINGS_FILEPATH, key='selected_mod_profile', value=None)
                    logging.warning(f'Deleted mod profile: {profile}')
                time.sleep(0.15)
                break


def fastflag_section() -> None:
    SECTIONS: list[str] = ['Go Back', 'Switch FastFlag Profiles', 'Configure FastFlag Profiles']

    while True:
        interface.open('FastFlags')

        index, response = interface.select(options=SECTIONS)

        if 'back' in response.lower() or 'return' in response.lower():
            return None

        elif 'switch' in response.lower():
            fastflag_section_switch()

        elif 'configure' in response.lower():
            fastflag_section_configure()


def fastflag_section_switch() -> None:
    SELECTED_ITEM_INDICATOR: str = variables.get('selected_item_indicator')
    CONFIG_DIRECTORY: str = variables.get('config_directory')
    FASTFLAG_PROFILES: dict = read_json.complete(filepath=os.path.join(CONFIG_DIRECTORY, 'fastflag_profiles.json'))

    while True:
        
        CURRENT_FASTFLAG_PROFILE: str = variables.get('selected_fastflag_profile')

        interface.open('Select a FastFlag profile')

        index, response = interface.select(
            ['Go Back'] + [profile if not profile == CURRENT_FASTFLAG_PROFILE else f'{CURRENT_FASTFLAG_PROFILE}{SELECTED_ITEM_INDICATOR}' for profile, fastflags in FASTFLAG_PROFILES.items()]
            + ['None' if CURRENT_FASTFLAG_PROFILE is not None else f'None{SELECTED_ITEM_INDICATOR}'],
            prompt='Select a FastFlag profile'
        )

        if response.lower() == 'go back':
            return None
        
        elif response.lower() == 'none':
            variables.set(name='selected_fastflag_profile', value=None)
            continue

        for profile, fastflags in FASTFLAG_PROFILES.items():
            if response == profile:
                variables.set(name='selected_fastflag_profile', value=response)


def fastflag_section_configure() -> None:
    CONFIG_DIRECTORY: str = variables.get('config_directory')

    while True:
        fastflag_profiles: dict = read_json.complete(filepath=os.path.join(CONFIG_DIRECTORY, 'fastflag_profiles.json'))

        interface.open('Configure FastFlag profiles')

        index, response = interface.select(
            ['Go Back'] + [profile for profile, fastflags in fastflag_profiles.items()] + ['Create New Profile'],
            prompt='Choose a FastFlag profile'
        )

        if response.lower() == 'go back':
            return None
        
        elif response.lower() == 'create new profile':
            interface.open('FastFlag Profile Creation')
            profile_name: str = interface.prompt(
                ['Choose a name for your new FastFlag profile'],
                restrict_responses=[profile for profile, fastflags in fastflag_profiles.items()]
            )
            write_json.value(filepath=os.path.join(CONFIG_DIRECTORY, 'fastflag_profiles.json'), key=profile_name, value={})
            logging.info(f'Created FastFlag profile: {profile_name}')

        for profile, fastflags in fastflag_profiles.items():
            if response == profile:
                
                logging.info(f'Configuring FastFlag profile: {response}')
                configure_fastflag_profile(response)


def configure_fastflag_profile(profile) -> None:
    SECTIONS: list[str] = ['Go Back', 'View FastFlags', 'Add FastFlags', 'Remove FastFlags', 'Rename FastFlag Profile', 'Delete FastFlag Profile']

    CONFIG_DIRECTORY: str = variables.get('config_directory')
    FASTFLAG_PROFILES_FILEPATH: str = os.path.join(CONFIG_DIRECTORY, 'fastflag_profiles.json')

    while True:
        fastflag_profiles: dict = read_json.complete(filepath=FASTFLAG_PROFILES_FILEPATH)

        interface.open(f'Mod profile: {profile}')

        index, response = interface.select(options=SECTIONS)

        if 'back' in response.lower() or 'return' in response.lower():
            return None

        elif 'view' in response.lower():  # View FastFlags in profile
            interface.open(f'Viewing FastFlags in {profile}')
            interface.text(
                [f'{name}: "{value}"' for name, value in sorted(fastflag_profiles[profile].items())]
                + ['']
            )
            input('Press ENTER to return . . .')

        elif 'add' in response.lower():  # Add FastFlags to profile
            interface.open(f'Add FastFlags to {profile}')
            name: str = interface.prompt('Enter the name of your FastFlag', response_spacing=0)
            value: str = interface.prompt(f'Enter the value for {name}', response_spacing=0)

            fastflags: dict = read_json.value(filepath=FASTFLAG_PROFILES_FILEPATH, key=profile)
            fastflags[name] = value
            write_json.value(filepath=FASTFLAG_PROFILES_FILEPATH, key=profile, value=fastflags)

        elif 'remove' in response.lower():  # Remove FastFlags from profile
            while True:
                interface.open(f'Remove FastFlag from: {profile}')

                fastflags: dict = read_json.value(filepath=FASTFLAG_PROFILES_FILEPATH, key=profile)

                index, response = interface.select(
                    ['Go Back']
                    + [fastflag for fastflag in fastflags],
                    prompt=f'Select a FastFlag to remove from: {profile}'
                )

                if response.lower() == 'go back':
                    break

                fastflags.pop(response)
                write_json.value(filepath=FASTFLAG_PROFILES_FILEPATH, key=profile, value=fastflags)
                logging.info(f'Removed FastFlag {response} from {profile}')

        elif 'rename' in response.lower():  # Rename FastFlag profile
            SETTINGS_FILEPATH: str = variables.get('settings_filepath')

            interface.open(f'Rename FastFlag profile: {profile}')

            new_profile_name: str = interface.prompt(
                ['Choose a new name for your FastFlag profile'],
                restrict_responses=[profile for profile, fastflags in fastflag_profiles.items()]
            )
            write_json.rename_key(filepath=FASTFLAG_PROFILES_FILEPATH, key=profile, name=new_profile_name)

            if variables.get('selected_fastflag_profile') == profile:
                variables.set(name='selected_fastflag_profile', value=new_profile_name)
            
            if read_json.value(filepath=SETTINGS_FILEPATH, key='selected_fastflag_profile') == profile:
                write_json.value(filepath=SETTINGS_FILEPATH, key='selected_fastflag_profile', value=new_profile_name)

            logging.info(f'Renamed FastFlag profile: {profile} -> {new_profile_name}')
            profile = new_profile_name

        elif 'delete' in response.lower():  # Delete FastFlag profile
            SETTINGS_FILEPATH: str = variables.get('settings_filepath')

            interface.open(f'Delete FastFlag profile {profile}')

            interface.text('CAUTION: This cannot be undone!')
            if interface.confirm(f'Are you sure you want to delete the following FastFlag profile: {profile}'):
                write_json.remove_key(filepath=FASTFLAG_PROFILES_FILEPATH, key=profile)
                if read_json.value(filepath=SETTINGS_FILEPATH, key='selected_fastflag_profile') == profile:
                    write_json.value(filepath=SETTINGS_FILEPATH, key='selected_fastflag_profile', value=None)
                    logging.warning(f'Deleted FastFlag profile: {profile}')
                time.sleep(0.15)
                break


def settings_section() -> None:
    while True:
        interface.open('Settings')
        settings: dict = variables.get('user_settings')
        index, response = interface.select(
            ['Go Back'] + [setting for setting, info in settings.items()],
            prompt='Choose a setting to change'
        )

        if 'back' in response.lower() or 'return' in response.lower():
            return None

        for setting, info in settings.items():
            if response == setting:
                interface.open(setting)
                interface.text(
                    [
                        f'Type: {info['type']}',
                        f'Description: {info['description']}',
                        f'Current value: {info['value']}'
                    ]
                )

                if info['type'] == 'toggle':
                    index, response = interface.select(options=[True, False], prompt='Choose a new value')
                    settings[setting]['value'] = response
                    variables.set(name='user_settings', value=settings)
                    time.sleep(0.15)

                elif info['type'] == 'number':
                    response = interface.select_number(prompt='Choose a new value', min=info['limit']['min'], max=info['limit']['max'])
                    settings[setting]['value'] = response
                    variables.set(name='user_settings', value=settings)
                    time.sleep(0.15)

                elif info['type'] == 'choice':
                    index, response = interface.select(options=info['options'], prompt='Choose a new value')
                    settings[setting]['value'] = response
                    variables.set(name='user_settings', value=settings)
                    time.sleep(0.15)
                
                logging.info(f'Changed setting {setting} ({info['type']}) to {response}')


def help_section() -> None:
    SECTIONS: list[str] = ['Go Back', 'Info', 'Useful Links', 'View License']

    while True:
        interface.open('Help')

        index, response = interface.select(options=SECTIONS)

        if 'back' in response.lower() or 'return' in response.lower():
            break

        elif 'info' in response.lower():
            help_section_info()

        elif 'links' in response.lower():
            help_section_links()

        elif 'license' in response.lower():
            help_section_license()


def help_section_info() -> None:
    interface.open('Project info')
    interface.text(
        [
            f'Project name: {variables.get('project_name')}',
            f'Project author: {variables.get('project_author')}',
            f'Project version: {variables.get('version')}',
            '',
            f'Installed Roblox version: {variables.get('installed_roblox_version')}',
            f'Selected mod profile: {variables.get('selected_mod_profile')}',
            f'Selected FastFlag profile: {variables.get('selected_fastflag_profile')}',
            ''
        ]
    )
    input('Press ENTER to return . . .')


def help_section_links() -> None:
    LINKS: dict = variables.get('links')

    interface.open('Links')
    index, response = interface.select(
        ['Go Back'] + [name for name, url in LINKS.items()],
        prompt='Select a link to open in your browser'
    )

    if 'back' in response.lower() or 'return' in response.lower():
        return None
    
    webbrowser.open(LINKS[response], new=2)


def help_section_license() -> None:
    interface.open('License')
    LICENSE_URL: str = r'https://raw.githubusercontent.com/TheKliko/klikos-modloader/main/LICENSE'
    license: str = request(LICENSE_URL, request_type='text')
    if not license:
        license = 'FAILED TO LOAD LICENSE, PLEASE TRY AGAIN\n'

    interface.text(license, spacing=0)
    input('Press ENTER to return . . .')


def save_changes() -> None:
    logging.debug('Saving changes...')
    SETTINGS_FILEPATH: str = variables.get('settings_filepath')

    SELECTED_MOD_PROFILE: str = variables.get('selected_mod_profile')
    CURRENT_MOD_PROFILE: str = read_json.value(filepath=SETTINGS_FILEPATH, key='selected_mod_profile')
    if SELECTED_MOD_PROFILE != CURRENT_MOD_PROFILE:
        variables.set(name='mod_profile_changed', value=True)
        write_json.value(filepath=SETTINGS_FILEPATH, key='selected_mod_profile', value=SELECTED_MOD_PROFILE)
    if variables.get('mod_profile_changed') and variables.get('roblox_reinstall_after_changes'):
        remove_version_directory()
        write_json.value(filepath=SETTINGS_FILEPATH, key='installed_roblox_version', value=None)
    
    SELECTED_FASTFLAG_PROFILE: str = variables.get('selected_fastflag_profile')
    write_json.value(filepath=SETTINGS_FILEPATH, key='selected_fastflag_profile', value=SELECTED_FASTFLAG_PROFILE)

    USER_SETTINGS: dict = variables.get('user_settings')
    write_json.value(filepath=SETTINGS_FILEPATH, key='user_settings', value=USER_SETTINGS)

    # Check for launch_roblox_after_setup
    if USER_SETTINGS['launch_roblox_after_setup']['value']:
        from modules.processes import startup
        startup.start()
        from modules.processes import launcher
        launcher.start()

def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()