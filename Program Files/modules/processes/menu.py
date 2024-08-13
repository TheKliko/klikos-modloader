# There's a lot of reused code in this one

import logging
import os
import re
import sys
import webbrowser
from tkinter.filedialog import askopenfilenames, asksaveasfilename

from modules import interface
from modules.utils import filesystem
from modules.utils import json_manager
from modules.utils import variables
from modules.utils import interface_response_validation as irv
from modules.presence.status import RichPresenceStatus


CANCEL: list[str] = [
    'go back',
    'return',
    'cancel'
]
BULLET: str = '\u2022'
SELECTED: str = ' <- [SELECTED]'
SECRET_INPUT_TRIGGER: list[str] = ['kliko', 'thekliko']
def secret_input_response() -> str:
    return variables.get('troubleshooting_urls')['secret']


def run() -> None:
    """Begin the menu process"""

    logging.info('Opening the modloader menu')
    variables.set('rpc_status', RichPresenceStatus.MENU)

    launch_configuration: dict = variables.get('launch_configuration')
    old_selected_mod_profile: str = launch_configuration['selected_mod_profile']
    variables.set('old_selected_mod_profile', old_selected_mod_profile)

    SECTIONS: list[str] = [
        'Save & Exit',
        'Choose Mod Profile',
        'Configure Mod Profiles',
        'FastFlags',
        'Settings',
        'About'
    ]
    while True:
        variables.remove('rpc_state')
        interface.open('Modloader Menu')
        interface.text(
            ['Select an option']
            + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
        )
        interface.divider()

        while True:
            response = interface.prompt()
            if irv.integer(response, 1, len(SECTIONS)):
                response = SECTIONS[int(response)-1]
                
                if response.lower() == 'save & exit':
                    variables.set('rpc_state', 'Shutting down...')
                    save_changes()
                    return
                
                elif response.lower() == 'choose mod profile':
                    choose_mod_profile()
                
                elif response.lower() == 'configure mod profiles':
                    variables.set('rpc_state', 'Configuring mods...')
                    configure_mod_profile()
                
                elif response.lower() == 'fastflags':
                    variables.set('rpc_state', 'Configuring FastFlags...')
                    fastflags()
                
                elif response.lower() == 'settings':
                    variables.set('rpc_state', 'Changing settings...')
                    settings()
                
                elif response.lower() == 'about':
                    about()

                break
            
            else:
                interface.open('Modloader Menu')
                interface.text(
                    ['Select an option']
                    + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
                )
                interface.divider()
                interface.text(
                    [
                        f'Invalid response: \'{response}\'',
                        f'Accepted responses are [1-{len(SECTIONS)}]'
                    ]
                )
                interface.divider()
                if response.lower() in SECRET_INPUT_TRIGGER:
                    webbrowser.open(secret_input_response(),2)


def choose_mod_profile() -> None:
    """Menu section"""
    
    SETTINGS_FILEPATH: str = variables.get('settings_filepath')
    MOD_PROFILES_FILEPATH: str = variables.get('mod_profiles_filepath')
    MOD_PROFILES: list[str] = json_manager.read(MOD_PROFILES_FILEPATH).keys()

    launch_configuration: dict = variables.get('launch_configuration')
    selected_mod_profile: str = launch_configuration['selected_mod_profile']

    while True:
        SECTIONS: list[str] = [
            'Go Back'
        ] + [
            profile if not profile == selected_mod_profile else f'{selected_mod_profile}{SELECTED}' for profile in MOD_PROFILES
        ] + [
            str(None) if not None == selected_mod_profile else f'{str(None)}{SELECTED}'
        ]

        interface.open('Modloader Menu | Mod Profiles')
        interface.text(
            ['Select an option']
            + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
        )
        interface.divider()

        while True:
            response = interface.prompt()
            if irv.integer(response, 1, len(SECTIONS)):
                response = SECTIONS[int(response)-1].removesuffix(SELECTED)

                if response.lower() == 'go back':
                    return

                selected_mod_profile = response
                if response == str(None):
                    selected_mod_profile = None
                launch_configuration['selected_mod_profile'] = selected_mod_profile

                json_manager.update(SETTINGS_FILEPATH, 'launch_configuration', launch_configuration)
                break

            else:
                interface.open('Modloader Menu | Mod Profiles')
                interface.text(
                    ['Select an option']
                    + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
                )
                interface.divider()
                interface.text(
                    [
                        f'Invalid response: \'{response}\'',
                        f'Accepted responses are [1-{len(SECTIONS)}]'
                    ]
                )
                interface.divider()
                if response.lower() in SECRET_INPUT_TRIGGER:
                    webbrowser.open(secret_input_response(),2)



def configure_mod_profile() -> None:
    """Menu section"""
    
    MOD_PROFILES_FILEPATH: str = variables.get('mod_profiles_filepath')

    while True:
        MOD_PROFILES: list[str] = json_manager.read(MOD_PROFILES_FILEPATH).keys()
        SECTIONS: list[str] = [
            'Go Back'
        ] + [
            profile for profile in MOD_PROFILES
        ] + [
            'Create New Profile'
        ]
        interface.open('Modloader Menu | Mod Profiles')
        interface.text(
            ['Select an option']
            + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
        )
        interface.divider()

        while True:
            response = interface.prompt()
            if irv.integer(response, 1, len(SECTIONS)):
                response = SECTIONS[int(response)-1]
                if response.lower() == 'go back':
                    return
                
                elif response.lower() == 'create new profile':
                    interface.open(
                        [
                            'Create a Mod Profile',
                            'Enter the name for this profile'
                        ]
                    )
                    interface.text(
                        [
                            'To cancel, enter one of the following items:'
                        ] + [f'{BULLET} \'{item}\'' for item in CANCEL]
                    )
                    interface.divider()
                    while True:
                        response = interface.prompt()
                        if response.lower() in CANCEL:
                            go_back = True
                            break

                        elif not response.lower() in [item.lower() for item in SECTIONS]:
                            json_manager.update(MOD_PROFILES_FILEPATH, response, {})
                            go_back = True
                            break

                        else:
                            interface.open(
                                [
                                    'Create a Mod Profile',
                                    'Enter the name for this profile'
                                ]
                            )
                            interface.text(
                                [
                                    'To cancel, enter one of the following items:'
                                ] + [f'{BULLET} \'{item}\'' for item in CANCEL]
                            )
                            interface.divider()
                            interface.text(
                                [
                                    f'Invalid response: \'{response}\'',
                                    f'Response may not be one of the following items:'
                                ] + [
                                    f'{BULLET} {item}' for item in SECTIONS
                                ]
                            )
                            interface.divider()
                    if go_back:
                        break

                else:
                    configure_selected_mod_profile(response)
                    break

            else:
                interface.open('Modloader Menu | Mod Profiles')
                interface.text(
                    ['Select an option']
                    + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
                )
                interface.divider()
                interface.text(
                    [
                        f'Invalid response: \'{response}\'',
                        f'Accepted responses are [1-{len(SECTIONS)}]'
                    ]
                )
                interface.divider()
                if response.lower() in SECRET_INPUT_TRIGGER:
                    webbrowser.open(secret_input_response(),2)


def configure_selected_mod_profile(profile: str) -> None:
    """Menu section"""
    
    MOD_PROFILES_FILEPATH: str = variables.get('mod_profiles_filepath')
    MODS_DIRECTORY: str = variables.get('mods_directory')

    while True:
        mod_profile_data: dict = json_manager.read(MOD_PROFILES_FILEPATH, profile)
        SECTIONS: list[str] = [
            'Go Back',
            'View Mods',
            'Add Mods',
            'Remove Mods',
            'Change Mod Priorities',
            'Rename Mod Profile',
            'Delete Mod Profile' 
        ]
        interface.open(f'Configure Mod Profile: {profile}')
        interface.text(
            ['Select an option']
            + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
        )
        interface.divider()

        while True:
            go_back: bool = False
            response = interface.prompt()
            if irv.integer(response, 1, len(SECTIONS)):
                response = SECTIONS[int(response)-1]
                if response.lower() == 'go back':
                    return


                elif response.lower() == 'view mods':
                    go_back = False
                    interface.open(
                        [
                            f'Mod Profile: {profile}',
                            'Viewing Mods'
                        ]
                    )

                    SETTINGS_FILEPATH: str = variables.get('settings_filepath')
                    USER_SETTINGS: dict = json_manager.read(SETTINGS_FILEPATH, 'user_settings')
                    PRIORITIES_IN_MOD_VIEW: bool = USER_SETTINGS['priorities_in_mod_view']['value']

                    if mod_profile_data == {}:
                        interface.text('No Mods Found!')

                    elif PRIORITIES_IN_MOD_VIEW:
                        interface.text(
                            [
                                f'{BULLET} {mod} [priority: {priority}]' for priority, mod in sorted(mod_profile_data.items(), key=lambda x: int(x[0]))
                            ]
                        )
                    
                    else:
                        interface.text(
                            [
                                f'{BULLET} {mod}' for mod in mod_profile_data.values()
                            ]
                        )

                    interface.divider()
                    interface.prompt('Press ENTER to return . . .')
                    break


                elif response.lower() == 'add mods':
                    go_back = False
                    while True:
                        mod_profile_config: dict = json_manager.read(MOD_PROFILES_FILEPATH, profile)
                        added_mods: list[str] = mod_profile_config.values()
                        installed_mods: list[str] = filesystem.subdirectories(MODS_DIRECTORY)

                        interface.open(
                            [
                                f'Mod Profile: {profile}',
                                'Add Mods'
                            ]
                        )
                        options: list[str] = [
                            'Go Back'
                        ] + [
                            mod for mod in installed_mods if not mod in added_mods
                        ]
                        interface.text(
                            [
                                f'Select a mod to add to \'{profile}\''
                            ] + [
                                f'[{options.index(option)+1}]: {option}' for option in options
                            ]
                        )
                        interface.divider()
                        while True:
                            response = interface.prompt()
                            if irv.integer(response, 1, len(options)):
                                response = options[int(response)-1]
                                if response.lower() == 'go back':
                                    go_back = True
                                    break
                            
                                priority: int = 1
                                while str(priority) in mod_profile_config:
                                    priority += 1
                                mod_profile_config[str(priority)] = response
                                json_manager.update(MOD_PROFILES_FILEPATH, profile, mod_profile_config)
                                break

                            else:
                                interface.open(
                                    [
                                        f'Mod Profile: {profile}',
                                        'Add Mods'
                                    ]
                                )
                                interface.text(
                                    [f'Select a mod to add to \'{profile}\'']
                                    + [f'[{options.index(option)+1}]: {option}' for option in options]
                                )
                                interface.divider()
                                interface.text(
                                    [
                                        f'Invalid response: \'{response}\'',
                                        f'Accepted responses are [1-{len(options)}]'
                                    ]
                                )
                                interface.divider()
                                if response.lower() in SECRET_INPUT_TRIGGER:
                                    webbrowser.open(secret_input_response(),2)

                        if go_back:
                            break


                elif response.lower() == 'remove mods':
                    go_back = False
                    while True:
                        mod_profile_config: dict = json_manager.read(MOD_PROFILES_FILEPATH, profile)
                        added_mods: list[str] = mod_profile_config.values()

                        interface.open(
                            [
                                f'Mod Profile: {profile}',
                                'Add Mods'
                            ]
                        )
                        options: list[str] = [
                            'Go Back'
                        ] + [
                            mod for mod in added_mods
                        ]
                        interface.text(
                            [
                                f'Select a mod to remove from \'{profile}\''
                            ] + [
                                f'[{options.index(option)+1}]: {option}' for option in options
                            ]
                        )
                        interface.divider()
                        while True:
                            response = interface.prompt()
                            if irv.integer(response, 1, len(options)):
                                response = options[int(response)-1]
                                if response.lower() == 'go back':
                                    go_back = True
                                    break
                            
                                new_mod_profile_config: dict = {priority: mod for priority, mod in sorted(mod_profile_config.items(), key=lambda x: int(x[0])) if not mod == response}
                                mod_profile_config = new_mod_profile_config
                                json_manager.update(MOD_PROFILES_FILEPATH, profile, new_mod_profile_config)
                                break

                            else:
                                interface.open(
                                    [
                                        f'Mod Profile: {profile}',
                                        'Add Mods'
                                    ]
                                )
                                interface.text(
                                    [f'Select a mod to remove from \'{profile}\'']
                                    + [f'[{options.index(option)+1}]: {option}' for option in options]
                                )
                                interface.divider()
                                interface.text(
                                    [
                                        f'Invalid response: \'{response}\'',
                                        f'Accepted responses are [1-{len(options)}]'
                                    ]
                                )
                                interface.divider()
                                if response.lower() in SECRET_INPUT_TRIGGER:
                                    webbrowser.open(secret_input_response(),2)
                            
                        if go_back:
                            break
                
                elif response.lower() == 'change mod priorities':
                    go_back = False
                    while True:
                        mod_profile_config: dict = json_manager.read(MOD_PROFILES_FILEPATH, profile)
                        mod_items: list[str] = mod_profile_config.items()

                        interface.open(
                            [
                                f'Mod Profile: {profile}',
                                'Edit Mod Priorities',
                                '(Mods get appled in order of priority [low -> high])'
                            ]
                        )
                        options: list[str] = [
                            'Go Back'
                        ] + [
                            f'{mod} [priority: {priority}]' for priority, mod in sorted(mod_items, key=lambda x: int(x[0]))
                        ]
                        interface.text(
                            [
                                f'Select a mod to change its priority'
                            ] + [
                                f'[{options.index(option)+1}]: {option}' for option in options
                            ]
                        )
                        interface.divider()
                        while True:
                            response = interface.prompt()
                            if irv.integer(response, 1, len(options)):
                                response = options[int(response)-1]

                                pattern = r' \[priority: -?\d+\]'
                                response = re.sub(pattern, '', response)
                                
                                if response.lower() == 'go back':
                                    go_back = True
                                    break

                                selected_mod: str = response
                                current_priority: str = next(priority for priority, mod in mod_items if mod == response)
                                interface.open(
                                    [
                                        f'Mod Profile: {profile}',
                                        f'Selected Mod: {selected_mod}',
                                        f'Current Priority: {current_priority}'
                                    ]
                                )
                                interface.text('Choose a new priority')
                                interface.divider()
                                while True:
                                    response = interface.prompt('New priority: ')
                                    if irv.integer(response):
                                        new_priority: str = response
                                        if current_priority == new_priority:
                                            pass

                                        elif not new_priority in mod_profile_config.keys():
                                            mod_profile_config[new_priority] = mod_profile_config.pop(current_priority)
                                        
                                        else:
                                            chosen_mod = mod_profile_config.pop(current_priority)
                                            
                                            mod_profile_config[str(current_priority)] = mod_profile_config[new_priority]
                                            mod_profile_config[new_priority] = chosen_mod
                                        
                                        json_manager.update(MOD_PROFILES_FILEPATH, profile, mod_profile_config)
                                        go_back = True
                                        break

                                    else:
                                        interface.open(
                                        [
                                            f'Mod Profile: {profile}',
                                            f'Selected Mod: {selected_mod}',
                                            f'Current Priority: {current_priority}'
                                        ]
                                        )
                                        interface.text('Choose a new priority')
                                        interface.divider()
                                        interface.text(
                                            [
                                                f'Invalid response: \'{response}\'',
                                                f'Response must be an integer'
                                            ]
                                        )
                                        interface.divider()
                                        if response.lower() in SECRET_INPUT_TRIGGER:
                                            webbrowser.open(secret_input_response(),2)
                                if go_back:
                                    go_back = False
                                    break

                            else:
                                interface.open(
                                    [
                                        f'Mod Profile: {profile}',
                                        'Edit Mod Priorities',
                                        '(Mods get appled in order of priority [low -> high])'
                                    ]
                                )
                                interface.text(
                                    [
                                        f'Select a mod to change its priority'
                                    ] + [
                                        f'[{options.index(option)+1}]: {option}' for option in options
                                    ]
                                )
                                interface.divider()
                                interface.text(
                                    [
                                        f'Invalid response: \'{response}\'',
                                        f'Accepted responses are [1-{len(options)}]'
                                    ]
                                )
                                interface.divider()
                                if response.lower() in SECRET_INPUT_TRIGGER:
                                    webbrowser.open(secret_input_response(),2)
                            
                        if go_back:
                            break
                
                elif response.lower() == 'rename mod profile':
                    go_back = False
                    mod_profiles: dict = json_manager.read(MOD_PROFILES_FILEPATH)
                    interface.open(
                        [
                            f'Mod Profile: {profile}',
                            'Rename Mod Profile'
                        ]
                    )
                    interface.text(
                        [
                            f'Choose a new name for \'{profile}\'',
                            'To cancel, enter one of the following items:'
                        ] + [
                            f'{BULLET} \'{item}\'' for item in CANCEL
                        ]
                    )
                    interface.divider()
                    while True:
                        response = interface.prompt()

                        if response.lower() in CANCEL:
                            go_back = True
                            break

                        elif response in mod_profiles.keys() and not response == profile:
                            interface.open(
                                [
                                    f'Mod Profile: {profile}',
                                    'Rename Mod Profile'
                                ]
                            )
                            interface.text(
                                [
                                    f'Choose a new name for \'{profile}\'',
                                    'To cancel, enter one of the following items:'
                                ] + [
                                    f'{BULLET} \'{item}\'' for item in CANCEL
                                ]
                            )
                            interface.divider()
                            interface.text(
                                [
                                    'Invalid response',
                                    '',
                                    'Response may not be one of the following items:'
                                ] + [
                                    f'{BULLET} {item}' for item in mod_profiles.keys() if not item == profile
                                ]
                            )
                            interface.divider()
                        
                        else:
                            mod_profiles[response] = mod_profiles.pop(profile)
                            json_manager.write(MOD_PROFILES_FILEPATH, mod_profiles)
                            
                            SETTINGS_FILEPATH: str = variables.get('settings_filepath')
                            launch_configuration = variables.get('launch_configuration')
                            launch_configuration['selected_mod_profile'] = response
                            json_manager.update(SETTINGS_FILEPATH, 'launch_configuration', launch_configuration)

                            old_selected_mod_profile: str = variables.get('old_selected_mod_profile')
                            if profile == old_selected_mod_profile:
                                variables.set('old_selected_mod_profile', response)
                            
                            profile = response
                            go_back = True
                        
                        if go_back:
                            break
                
                elif response.lower() == 'delete mod profile':
                    go_back = False
                    mod_profiles: dict = json_manager.read(MOD_PROFILES_FILEPATH)
                    interface.open(
                                [
                                    f'Mod Profile: {profile}',
                                    'Delete Mod Profile'
                                ]
                    )
                    interface.text(
                        [
                            'Are you sure you want to permanently delete this mod profile? [Y/N]',
                            '',
                            '[CAUTION]: This cannot be undone!'
                        ]
                    )
                    interface.divider()
                    response = interface.prompt()
                    validation: tuple = irv.boolean(response)
                    is_bool: bool = validation[0]
                    result: bool = validation[1]

                    if is_bool == True and result == True:
                        mod_profiles.pop(profile)
                        json_manager.write(MOD_PROFILES_FILEPATH, mod_profiles)
                        return

                    elif is_bool == True and result == False:
                        break

                    else:
                        interface.open(
                            [
                                f'Mod Profile: {profile}',
                                'Delete Mod Profile'
                            ]
                        )
                        interface.text(
                            [
                                'Are you sure you want to permanently delete this mod profile? [Y/N]',
                                '',
                                '[CAUTION]: This cannot be undone!'
                            ]
                        )
                        interface.divider()
                        interface.text(
                            [
                                f'Invalid response: \'{response}\'',
                                f'Accepted responses are [Y/N]'
                            ]
                        )
                        interface.divider()
                        interface.prompt('Press ENTER to return . . .')
                        

                    go_back = True

                if go_back:
                    break

            else:
                interface.open(f'Configure Mod Profile: {profile}')
                interface.text(
                    ['Select an option']
                    + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
                )
                interface.divider()
                interface.text(
                    [
                        f'Invalid response: \'{response}\'',
                        f'Accepted responses are [1-{len(SECTIONS)}]'
                    ]
                )
                interface.divider()
                if response.lower() in SECRET_INPUT_TRIGGER:
                    webbrowser.open(secret_input_response(),2)


def fastflags() -> None:
    """Menu section"""
    
    SECTIONS: list[str] = [
        'Go Back',
        'Choose FastFlag Profile',
        'Configure FastFlag Profiles'
    ]

    while True:
        interface.open('Modloader Menu | FastFlags')
        interface.text('Select an option')
        interface.text([f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS])
        interface.divider()
        while True:
            response = interface.prompt()
            if irv.integer(response, 1, len(SECTIONS)):
                    response = SECTIONS[int(response)-1]
                    if response.lower() == 'go back':
                        return

                    elif response.lower() == 'choose fastflag profile':
                        choose_fastflag_profile()

                    elif response.lower() == 'configure fastflag profiles':
                        configure_fastflag_profile()
                    break
            
            else:
                interface.open('Modloader Menu | FastFlags')
                interface.text('Select an option')
                interface.text([f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS])
                interface.divider()
                interface.text(
                    [
                        f'Invalid response: \'{response}\'',
                        f'Accepted responses are [1-{len(SECTIONS)}]'
                    ]
                )
                interface.divider()
                if response.lower() in SECRET_INPUT_TRIGGER:
                    webbrowser.open(secret_input_response(),2)


def choose_fastflag_profile() -> None:
    """Menu section"""
    
    SETTINGS_FILEPATH: str = variables.get('settings_filepath')
    FASTFLAG_PROFILES_FILEPATH: str = variables.get('fastflag_profiles_filepath')
    FASTFLAG_PROFILES: dict = json_manager.read(FASTFLAG_PROFILES_FILEPATH).keys()
    launch_configuration: dict = variables.get('launch_configuration')
    selected_fastflag_profile: str = launch_configuration['selected_fastflag_profile']

    while True:
        SECTIONS: list[str] = [
            'Go back'
        ] + [
            profile if not profile == selected_fastflag_profile else f'{selected_fastflag_profile}{SELECTED}' for profile in FASTFLAG_PROFILES
        ] + [
            str(None) if not None == selected_fastflag_profile else f'{str(None)}{SELECTED}'
        ]

        interface.open('Modloader Menu | FastFlag Profiles')
        interface.text('Select an option')
        interface.text([f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS])
        interface.divider()


        while True:
            response = interface.prompt()
            if irv.integer(response, 1, len(SECTIONS)):
                response = SECTIONS[int(response)-1].removesuffix(SELECTED)

                if response.lower() == 'go back':
                    return
                
                selected_fastflag_profile = response

                if response == str(None):
                    selected_fastflag_profile = None
                launch_configuration['selected_fastflag_profile'] = selected_fastflag_profile

                json_manager.update(SETTINGS_FILEPATH, 'launch_configuration', launch_configuration)
                break

            else:
                interface.open('Modloader Menu | FastFlag Profiles')
                interface.text(
                    ['Select an option']
                    + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
                )
                interface.divider()
                interface.text(
                    [
                        f'Invalid response: \'{response}\'',
                        f'Accepted responses are [1-{len(SECTIONS)}]'
                    ]
                )
                interface.divider()
                if response.lower() in SECRET_INPUT_TRIGGER:
                    webbrowser.open(secret_input_response(),2)


def configure_fastflag_profile() -> None:
    """Menu section"""
    
    FASTFLAG_PROFILES_FILEPATH: str = variables.get('fastflag_profiles_filepath')

    while True:
        FASTFLAG_PROFILES: list[str] = json_manager.read(FASTFLAG_PROFILES_FILEPATH).keys()
        SECTIONS: list[str] = [
            'Go Back'
        ] + [
            profile for profile in FASTFLAG_PROFILES
        ] + [
            'Create New Profile'
        ]
        interface.open('Modloader Menu | FastFlag Profiles')
        interface.text(
            ['Select an option']
            + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
        )
        interface.divider()

        while True:
            response = interface.prompt()
            if irv.integer(response, 1, len(SECTIONS)):
                response = SECTIONS[int(response)-1]
                if response.lower() == 'go back':
                    return
                
                elif response.lower() == 'create new profile':
                    interface.open(
                        [
                            'Create a FastFlag Profile',
                            'Enter the name for this profile'
                        ]
                    )
                    interface.text(
                        [
                            'To cancel, enter one of the following items:'
                        ] + [f'{BULLET} \'{item}\'' for item in CANCEL]
                    )
                    interface.divider()
                    while True:
                        response = interface.prompt()
                        if response.lower() in CANCEL:
                            go_back = True
                            break

                        elif not response.lower() in [item.lower() for item in SECTIONS]:
                            json_manager.update(FASTFLAG_PROFILES_FILEPATH, response, {})
                            go_back = True
                            break

                        else:
                            interface.open(
                                [
                                    'Create a FastFlag Profile',
                                    'Enter the name for this profile'
                                ]
                            )
                            interface.text(
                                [
                                    'To cancel, enter one of the following items:'
                                ] + [f'{BULLET} \'{item}\'' for item in CANCEL]
                            )
                            interface.divider()
                            interface.text(
                                [
                                    f'Invalid response: \'{response}\'',
                                    f'Response may not be one of the following items:'
                                ] + [
                                    f'{BULLET} {item}' for item in SECTIONS
                                ]
                            )
                            interface.divider()
                    if go_back:
                        break

                else:
                    configure_selected_fastflag_profile(response)
                    break

            else:
                interface.open('Modloader Menu | FastFlag Profiles')
                interface.text(
                    ['Select an option']
                    + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
                )
                interface.divider()
                interface.text(
                    [
                        f'Invalid response: \'{response}\'',
                        f'Accepted responses are [1-{len(SECTIONS)}]'
                    ]
                )
                interface.divider()
                if response.lower() in SECRET_INPUT_TRIGGER:
                    webbrowser.open(secret_input_response(),2)


def configure_selected_fastflag_profile(profile: str) -> None:
    """Menu section"""
    
    FASTFLAG_PROFILES_FILEPATH: str = variables.get('fastflag_profiles_filepath')

    while True:
        fastflag_profile_data: dict = json_manager.read(FASTFLAG_PROFILES_FILEPATH, profile)
        SECTIONS: list[str] = [
            'Go Back',
            'View FastFlags',
            'Add FastFlags',
            'Remove FastFlags',
            'Import FastFlags',
            'Export FastFlags',
            'Rename FastFlag Profile',
            'Delete FastFlag Profile'
        ]

        interface.open(f'Configure FastFlag Profile: {profile}')
        interface.text('Select an option')
        interface.text([f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS])
        interface.divider()
        while True:
            go_back: bool = False
            response = interface.prompt()
            if irv.integer(response, 1, len(SECTIONS)):
                response = SECTIONS[int(response)-1]
                if response.lower() == 'go back':
                    return
                
                elif response.lower() == 'view fastflags':
                    go_back = False
                    interface.open(
                        [
                            f'FastFlag Profile: {profile}',
                            'Viewing FastFlags'
                        ]
                    )

                    SETTINGS_FILEPATH: str = variables.get('settings_filepath')
                    if fastflag_profile_data == {}:
                        interface.text('No FastFlags Found!')
                    else:
                        interface.text(
                            [f'\"{name}\": \"{value}\"' for name, value in fastflag_profile_data.items()]
                        )
                    interface.divider()
                    interface.prompt('Press ENTER to return . . .')
                    break
                    
                elif response.lower() == 'add fastflags':
                    go_back = False
                    while True:
                        fastflag_profile_config: dict = json_manager.read(FASTFLAG_PROFILES_FILEPATH, profile)
                        added_fastflags: list[str] = [key for key in fastflag_profile_config.keys()]

                        interface.open([f'FastFlag Profile: {profile}','Add FastFlags'])
                        interface.text(
                            [
                                f'Enter the name of the FastFlag you wish to add to \'{profile}\'',
                                'Existing values will be overwritten'
                            ]
                        )
                        interface.divider()
                        interface.text(
                            [
                                'To cancel, enter one of the following items:'
                            ] + [f'{BULLET} \'{item}\'' for item in CANCEL]
                        )
                        interface.divider()
                        response = interface.prompt()
                        if response.lower() in CANCEL:
                            break

                        fastflag = response
                        interface.open([f'FastFlag Profile: {profile}','Add FastFlags'])
                        interface.text(
                            [
                                f'Enter the value for \"{fastflag}\"',
                                'Existing values will be overwritten'
                            ]
                        )
                        interface.divider()
                        interface.text(
                            [
                                'To cancel, enter one of the following items:'
                            ] + [f'{BULLET} \'{item}\'' for item in CANCEL]
                        )
                        interface.divider()
                        response = interface.prompt()
                        if response.lower() in CANCEL:
                            break
                        
                        else:
                            value = response
                            fastflag_profile_config[fastflag] = value
                            json_manager.update(FASTFLAG_PROFILES_FILEPATH, profile, fastflag_profile_config)

                    break
                    
                elif response.lower() == 'remove fastflags':
                    go_back = False
                    while True:
                        fastflag_profile_config: dict = json_manager.read(FASTFLAG_PROFILES_FILEPATH, profile)
                        added_fastflags: list[str] = [key for key in fastflag_profile_config.keys()]

                        interface.open([f'FastFlag Profile: {profile}','Add FastFlags'])
                        options: list[str] = ['Go Back'] + [
                            fastflag for fastflag in added_fastflags
                        ]
                        interface.text(f'Enter the name of the FastFlag you wish to remove from \'{profile}\'')
                        interface.text([f'[{options.index(option)+1}]: {option}' for option in options])
                        interface.divider()
                        while True:
                            response = interface.prompt()
                            if irv.integer(response, 1, len(options)):
                                response = options[int(response)-1]
                                if response.lower() == 'go back':
                                    go_back = True
                                    break

                                fastflag_profile_config.pop(response)
                                json_manager.update(FASTFLAG_PROFILES_FILEPATH, profile, fastflag_profile_config)
                                break

                            else:
                                interface.open([f'FastFlag Profile: {profile}','Add FastFlags'])
                                options: list[str] = ['Go Back'] + [
                                    fastflag for fastflag in added_fastflags
                                ]
                                interface.text(f'Enter the name of the FastFlag you wish to remove from \'{profile}\'')
                                interface.text([f'[{options.index(option)+1}]: {option}' for option in options])
                                interface.divider()
                                interface.text(f'Invalid response: \'{response}\'')
                                interface.text(f'Accepted responses are [1-{len(options)}]')
                                interface.divider()
                    
                        if go_back:
                            break
                    
                elif response.lower() == 'import fastflags':
                    go_back = False
                    fastflag_profile_config: dict = json_manager.read(FASTFLAG_PROFILES_FILEPATH, profile)
                    target = askopenfilenames(
                        filetypes=[('JSON files', '*.json')],
                        initialdir=os.path.join(os.getenv('HOME') or os.getenv('USERPROFILE'), 'Downloads'),
                        initialfile='ClientAppSettings.json',
                        title='Import FastFlags'
                    )

                    if isinstance(target, tuple):
                        for item in target:
                            try:
                                fastflags = json_manager.read(item)
                                for key, value in fastflags.items():
                                    fastflag_profile_config[key] = value
                                    json_manager.update(FASTFLAG_PROFILES_FILEPATH, profile, fastflag_profile_config)
                            except Exception as e:
                                interface.open([f'FastFlag Profile: {profile}','Add FastFlags'])
                                interface.text(
                                    [
                                        f'Failed to import FastFlags from {os.path.basename(item)}',
                                        f'An unexpected {type(e).__name__} occured:',
                                        str(e)
                                    ],
                                    alignment=interface.Aligntment.center
                                )
                                interface.divider()
                                interface.prompt('Press ENTER to continue . . .')
                    break
                    
                elif response.lower() == 'export fastflags':
                    fastflag_profile_config: dict = json_manager.read(FASTFLAG_PROFILES_FILEPATH, profile)
                    target = asksaveasfilename(
                        filetypes=[('JSON files', '*.json')],
                        initialdir=os.path.join(os.getenv('HOME') or os.getenv('USERPROFILE'), 'Downloads'),
                        initialfile='ClientAppSettings.json',
                        title='Export FastFlags'
                    )

                    if isinstance(target, str):
                        json_manager.write(target, fastflag_profile_config)
                    break
                    
                elif response.lower() == 'rename fastflag profile':
                    go_back = False
                    fastflag_profiles: dict = json_manager.read(FASTFLAG_PROFILES_FILEPATH)
                    interface.open([f'FastFlag Profile: {profile}', 'Rename FastFlag Profile'])
                    interface.text([f'Choose a new name for \'{profile}\'', 'To cancel, enter one of the following items:'])
                    interface.text([f'{BULLET} \'{item}\'' for item in CANCEL])
                    interface.divider()
                    while True:
                        response = interface.prompt()

                        if response.lower() in CANCEL:
                            go_back = True
                            break

                        elif response in fastflag_profiles.keys() and not response == profile:
                            interface.open(
                                [
                                    f'FastFlag Profile: {profile}',
                                    'Rename FastFlag Profile'
                                ]
                            )
                            interface.text(
                                [
                                    f'Choose a new name for \'{profile}\'',
                                    'To cancel, enter one of the following items:'
                                ] + [
                                    f'{BULLET} \'{item}\'' for item in CANCEL
                                ]
                            )
                            interface.divider()
                            interface.text(
                                [
                                    'Invalid response',
                                    '',
                                    'Response may not be one of the following items:'
                                ] + [
                                    f'{BULLET} {item}' for item in fastflag_profiles.keys() if not item == profile
                                ]
                            )
                            interface.divider()
                        
                        else:
                            fastflag_profiles[response] = fastflag_profiles.pop(profile)
                            json_manager.write(FASTFLAG_PROFILES_FILEPATH, fastflag_profiles)
                            
                            SETTINGS_FILEPATH: str = variables.get('settings_filepath')
                            launch_configuration = variables.get('launch_configuration')
                            launch_configuration['selected_fastflag_profile'] = response
                            json_manager.update(SETTINGS_FILEPATH, 'launch_configuration', launch_configuration)
                            
                            profile = response
                            go_back = True
                        
                        if go_back:
                            break
                
                elif response.lower() == 'delete fastflag profile':
                    go_back = False
                    fastflag_profiles: dict = json_manager.read(FASTFLAG_PROFILES_FILEPATH)
                    interface.open(
                                [
                                    f'FastFlag Profile: {profile}',
                                    'Delete FastFlag Profile'
                                ]
                    )
                    interface.text(
                        [
                            'Are you sure you want to permanently delete this fastflag profile? [Y/N]',
                            '',
                            '[CAUTION]: This cannot be undone!'
                        ]
                    )
                    interface.divider()
                    response = interface.prompt()
                    validation: tuple = irv.boolean(response)
                    is_bool: bool = validation[0]
                    result: bool = validation[1]

                    if is_bool == True and result == True:
                        fastflag_profiles.pop(profile)
                        json_manager.write(FASTFLAG_PROFILES_FILEPATH, fastflag_profiles)
                        return

                    elif is_bool == True and result == False:
                        break

                    else:
                        interface.open(
                            [
                                f'FastFlag Profile: {profile}',
                                'Delete FastFlag Profile'
                            ]
                        )
                        interface.text(
                            [
                                'Are you sure you want to permanently delete this fastflag profile? [Y/N]',
                                '',
                                '[CAUTION]: This cannot be undone!'
                            ]
                        )
                        interface.divider()
                        interface.text(
                            [
                                f'Invalid response: \'{response}\'',
                                f'Accepted responses are [Y/N]'
                            ]
                        )
                        interface.divider()
                        interface.prompt('Press ENTER to return . . .')
                        

                    go_back = True

                if go_back:
                    break
                


            else:
                interface.open('Configure FastFlag Profile: {profile}')
                interface.text('Select an option')
                interface.text([f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS])
                interface.divider()
                interface.text(
                    [
                        f'Invalid response: \'{response}\'',
                        f'Accepted responses are [1-{len(SECTIONS)}]'
                    ]
                )
                interface.divider()
                if response.lower() in SECRET_INPUT_TRIGGER:
                    webbrowser.open(secret_input_response(),2)
            if go_back:
                break



def settings() -> None:
    """Menu section"""

    SETTINGS_FILEPATH: str = variables.get('settings_filepath')
    while True:
        settings: dict = json_manager.read(SETTINGS_FILEPATH, 'user_settings')
        SECTIONS: list[str] = [
            'Go Back'
        ] + [data['name'] for setting, data in settings.items()]

        interface.open('Modloader Menu | Settings')
        interface.text(
            ['Select an option']
            + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
        )
        interface.divider()
        while True:
            response = interface.prompt()
            if irv.integer(response, 1, len(SECTIONS)):
                response = SECTIONS[int(response)-1]
                if response.lower() == 'go back':
                    go_back = True
                    break

                setting = next(setting for setting, data in settings.items() if data['name'] == response)

                interface.open(
                    [
                        'Modloader Menu | Settings',
                        settings[setting]['name']
                    ]
                )
                interface.text(
                    [
                        f'Name: {settings[setting]['name']}',
                        f'Description: {settings[setting]['description'].replace('{project_name}', variables.get('project_data')['name'])}',
                        f'Type: {settings[setting]['type']}',
                        f'Current Value: {settings[setting]['value']}',
                        f'Default value: {settings[setting]['default']}'
                    ]
                )
                interface.divider()
                interface.text(
                    [
                        'Please choose a new value',
                        'To cancel, enter one of the following items:'
                    ] + [
                        f'{BULLET} \'{item}\'' for item in CANCEL
                    ]
                )
                interface.divider()
                while True:
                    response = interface.prompt()
                    if response.lower() in CANCEL:
                        go_back = True
                        break

                    if settings[setting]['type'] == 'boolean':
                        validation: tuple = irv.boolean(response)
                        is_bool: bool = validation[0]
                        result: bool = validation[1]

                        if is_bool == True and result == True:
                            settings[setting]['value'] = True
                            json_manager.update(SETTINGS_FILEPATH, 'user_settings', settings)
                            go_back = True
                            break

                        elif is_bool == True and result == False:
                            settings[setting]['value'] = False
                            json_manager.update(SETTINGS_FILEPATH, 'user_settings', settings)
                            go_back = True
                            break

                        else:
                            interface.open(
                                [
                                    'Modloader Menu | Settings',
                                    settings[setting]['name']
                                ]
                            )
                            interface.text(
                                [
                                    f'Name: {settings[setting]['name']}',
                                    f'Description: {settings[setting]['description'].replace('{project_name}', variables.get('project_data')['name'])}',
                                    f'Type: {settings[setting]['type']}',
                                    f'Current Value: {settings[setting]['value']}',
                                    f'Default value: {settings[setting]['default']}'
                                ]
                            )
                            interface.divider()
                            interface.text(
                                [
                                    'Please choose a new value',
                                    'To cancel, enter one of the following items:'
                                ] + [
                                    f'{BULLET} \'{item}\'' for item in CANCEL
                                ]
                            )
                            interface.divider()
                            interface.text(
                                [
                                    f'Invalid response: \'{response}\'',
                                    'Accepted responses are [Y/N]'
                                ]
                            )
                            interface.divider()
                            if response.lower() in SECRET_INPUT_TRIGGER:
                                webbrowser.open(secret_input_response(),2)

                    elif settings[setting]['type'] == 'integer':
                        if irv.integer(response, settings[setting]['range']['min'], settings[setting]['range']['max']):
                            settings[setting]['value'] = int(response)
                            json_manager.update(SETTINGS_FILEPATH, 'user_settings', settings)
                            go_back = True
                            break

                        else:
                            interface.open(
                                [
                                    'Modloader Menu | Settings',
                                    settings[setting]['name']
                                ]
                            )
                            interface.text(
                                [
                                    f'Name: {settings[setting]['name']}',
                                    f'Description: {settings[setting]['description'].replace('{project_name}', variables.get('project_data')['name'])}',
                                    f'Type: {settings[setting]['type']}',
                                    f'Current Value: {settings[setting]['value']}',
                                    f'Default value: {settings[setting]['default']}'
                                ]
                            )
                            interface.divider()
                            interface.text(
                                [
                                    'Please choose a new value',
                                    'To cancel, enter one of the following items:'
                                ] + [
                                    f'{BULLET} \'{item}\'' for item in CANCEL
                                ]
                            )
                            interface.divider()
                            if settings[setting]['range']['min'] and settings[setting]['range']['max']:
                                interface.text(
                                    [
                                        f'Invalid response: \'{response}\'',
                                        f'Accepted responses are [{settings[setting]['range']['min']}-{settings[setting]['range']['max']}]'
                                    ]
                                )
                            elif settings[setting]['range']['min'] and not settings[setting]['range']['max']:
                                interface.text(
                                    [
                                        f'Invalid response: \'{response}\'',
                                        f'Accepted responses are [{settings[setting]['range']['min']} or higher]'
                                    ]
                                )
                            elif not settings[setting]['range']['min'] and settings[setting]['range']['max']:
                                interface.text(
                                    [
                                        f'Invalid response: \'{response}\'',
                                        f'Accepted responses are [{settings[setting]['range']['max']} or lower]'
                                    ]
                                )
                            else:
                                interface.text(
                                    [
                                        f'Invalid response: \'{response}\'',
                                        f'Accepted responses are integers'
                                    ]
                                )
                            interface.divider()
                            if response.lower() in SECRET_INPUT_TRIGGER:
                                webbrowser.open(secret_input_response(),2)

            
            else:
                interface.open('Modloader Menu | Settings')
                interface.text(
                    ['Select an option']
                    + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
                )
                interface.divider()
                interface.text(
                    [
                        f'Invalid response: \'{response}\'',
                        f'Accepted responses are [1-{len(SECTIONS)}]'
                    ]
                )
                interface.divider()
                if response.lower() in SECRET_INPUT_TRIGGER:
                    webbrowser.open(secret_input_response(),2)
                
            if go_back:  # If it's stupid but it works, it's not stupid
                go_back = False
                break
            
        if go_back:
            break


def about() -> None:
    """Menu section"""
    
    SETTINGS_FILEPATH: str = variables.get('settings_filepath')
    LICENSES: dict = json_manager.read(SETTINGS_FILEPATH, 'licenses')
    PROJECT_DATA: dict = variables.get('project_data')
    USER_SETTINGS: dict = json_manager.read(SETTINGS_FILEPATH, 'user_settings')
    TROUBLESHOOTING_URLS: dict = variables.get('troubleshooting_urls')

    SECTIONS: list[str] = [
        'Go Back',
        'Project Info',
        'View License',
        'Help',
    ]

    while True:
        interface.open('Modloader Menu | About')
        interface.text(
                ['Select an option']
                + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
        )
        interface.divider()
        while True:
            response = interface.prompt()
            if irv.integer(response, 1, len(SECTIONS)):
                response = SECTIONS[int(response)-1]
                if response.lower() == 'go back':
                    go_back = True
                    break

                elif response.lower() == 'project info':
                    interface.open('Project Info')
                    interface.text(
                        [
                            f'Name: {PROJECT_DATA['name']}',
                            f'Made by: {PROJECT_DATA['author']}',
                            f'Version: {PROJECT_DATA['version']}',
                            f'Description: {PROJECT_DATA['description']}'
                        ]
                    )
                    interface.divider()
                    interface.text(
                        [
                            'User settings:'
                        ] + [
                            f'{BULLET} [{name}] [{data['value']}]' for name, data in USER_SETTINGS.items()
                        ]
                    )
                    interface.divider()
                    interface.prompt('Press ENTER to return')
                    go_back = False
                    break

                elif response.lower() == 'view license':
                    variables.set('rpc_state', 'Viewing license...')
                    interface.open('Viewing Licenses')
                    for name, data in LICENSES.items():
                        name = name.replace(r'{project_name}', PROJECT_DATA['name'])

                        if USER_SETTINGS['show_short_license']['value']:
                            interface.text(
                                [
                                    f'License: {name}',
                                    f'Type: {data['type']}'
                                ]
                            )
                        else:
                            interface.text(
                                [
                                    f'License: {name}',
                                    f'Type: {data['type']}',
                                    f''
                                ] + data['text']
                            )

                        interface.divider()
                    interface.prompt('Press ENTER to return')
                    variables.remove('rpc_state')
                    go_back = False
                    break

                elif response.lower() == 'help':
                    interface.open('Help & Support')
                    interface.text('CTRL + CLICK on the following URLs to open them in your browser')
                    interface.newline()
                    interface.text(
                        [
                            'Discord server:',
                            f'{BULLET} {TROUBLESHOOTING_URLS['discord']}',
                            '',
                            'Official website:',
                            f'{BULLET} {TROUBLESHOOTING_URLS['website']}',
                            '',
                            'GitHub repository:',
                            f'{BULLET} {TROUBLESHOOTING_URLS['github']}'
                        ]
                    )
                    interface.divider()
                    interface.prompt('Press ENTER to return')
                    go_back = False
                    break
            
            else:
                interface.open('Modloader Menu | Settings')
                interface.text(
                    ['Select an option']
                    + [f'[{SECTIONS.index(section)+1}]: {section}' for section in SECTIONS]
                )
                interface.divider()
                interface.text(
                    [
                        f'Invalid response: \'{response}\'',
                        f'Accepted responses are [1-{len(SECTIONS)}]'
                    ]
                )
                interface.divider()
                if response.lower() in SECRET_INPUT_TRIGGER:
                    webbrowser.open(secret_input_response(),2)

        
        if go_back:
            break


def save_changes() -> None:
    """Save changes and exit the menu process"""

    logging.info('Saving changes')
    launch_configuration: dict = variables.get('launch_configuration')
    old_selected_mod_profile: str = variables.get('old_selected_mod_profile')

    SETTINGS_FILEPATH: str = variables.get('settings_filepath')
    user_settings: dict = json_manager.read(SETTINGS_FILEPATH, 'user_settings')
    new_selected_mod_profile: str = json_manager.read(SETTINGS_FILEPATH, 'launch_configuration')['selected_mod_profile']

    if user_settings['roblox_reinstall_after_changes']['value'] == True and old_selected_mod_profile != new_selected_mod_profile and old_selected_mod_profile != None:
        launch_configuration['force_roblox_reinstallation'] = True
    
    if user_settings['roblox_force_reinstall']['value'] == True:
        launch_configuration['force_roblox_reinstallation'] = True
        user_settings['roblox_force_reinstall']['value'] == False
    
    json_manager.update(SETTINGS_FILEPATH, 'user_settings', user_settings)
    json_manager.update(SETTINGS_FILEPATH, 'launch_configuration', launch_configuration)


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()