import json
import os
from tkinter.filedialog import askopenfilenames, asksaveasfilename

from modules import interface
from modules.other.response import Response

from .. import fastflag_data


class Break(Exception):
    pass


def show(window: interface.Interface) -> str:
    while True:
        window.change_section_description()
        window.reset()

        try:
            profiles: list[dict] = fastflag_data.get_all()
        except Exception as e:
            window.add_line('Section failed to load!', color=interface.Color.WARNING)
            window.add_line(f'[{type(e).__name__}]: {str(e)}', color=interface.Color.ERROR)
            window.add_divider()
            window.get_input('Press ENTER to return . . .')
            return 'home'


        options: list = [
            'Go Back',
            'Create New Profile'
        ] + [
            f'{interface.foreground(interface.Color.ON)}+{interface.Color.DEFAULT} {profile.get('name', 'ERROR_FAILED_TO_LOAD')}'
            if profile.get('enabled', False) == True
            else f'{interface.foreground(interface.Color.OFF)}-{interface.Color.DEFAULT} {profile.get('name', 'ERROR_FAILED_TO_LOAD')}'
            for profile in profiles
        ]
        for i, option in enumerate(options, start=1):
            window.add_line(f'[{i}]:{f" " if i < 10 else ""} {option}')
        window.add_divider()

        bad_input: bool = False
        while True:
            response: str = window.get_input('Response: ')
            try:
                i = int(response)
                if i > 0 and i <= len(options):
                    if i == 1:
                        return 'home'
                    response = ' '.join(options[i-1].split(' ')[1:])
                    break
            except:
                pass

            if bad_input != False:
                window.remove_last(3)
            window.add_line(f'Invalid response: "{response}"')
            window.add_line(f'Accepted answers are: [1-{len(options)}]')
            window.add_divider()
            bad_input = True
            window._on_update()
        
        if i == 2:
            response = create_new_profile(window, profiles)
        configure(window, response)


def create_new_profile(window: interface.Interface, profiles: list) -> str:
    window.add_line('Please choose a name for your new FastFlag profile!')
    window.add_divider()

    bad_input = False
    while True:
        response: str = window.get_input('Response: ')
        if response not in [profile.get('name', None) for profile in profiles]:
            fastflag_data.new(response)
            return response

        if bad_input != False:
            window.remove_last(3)
        window.add_line(f'Invalid response: "{response}"')
        window.add_line(f'Profile may not share the same name as another FastFlag profile!')
        window.add_divider()
        bad_input = True
        window._on_update()


def configure(window: interface.Interface, profile: str) -> None:
    while True:
        window.change_section_description(f' > {profile}')
        window.reset()

        try:
            data: dict = fastflag_data.get(profile) 
        except Exception as e:
            window.add_line('Section failed to load!', color=interface.Color.WARNING)
            window.add_line(f'[{type(e).__name__}]: {str(e)}', color=interface.Color.ERROR)
            window.add_divider()
            window.get_input('Press ENTER to return . . .')
            return

        description: int = data.get('description', None)
        enabled: bool = data.get('enabled', False)
        fastflags: dict = data.get('data', {})

        window.add_line(f'Name: {profile}')
        window.add_line(f'Description: {description if description != '' else None}')
        window.add_line(f'Status: {f'{interface.foreground(interface.Color.ON)}[enabled]{interface.Color.DEFAULT}' if enabled == True else f'{interface.foreground(interface.Color.OFF)}[disabled]{interface.Color.DEFAULT}'}')
        window.add_line(' ')
        window.add_line('Data:')
        window.add_line('{')
        for key, value in fastflags.items():
            window.add_line(f'  {'"' if isinstance(key, str) else ''}{key}{'"' if isinstance(key, str) else ''}: {'"' if isinstance(value, str) else ''}{value}{'"' if isinstance(value, str) else ''}{',' if key != list(fastflags.keys())[-1] else ''}')
        if fastflags == {}:
            window.add_line('  NO_DATA')
        window.add_line('}')
        window.add_divider()

        options: list = [
            'Go Back',
            'Toggle status',
            'Change profile name',
            'Change profile description',
            'Add FastFlags',
            'Remove FastFlags',
            'Import FastFlags',
            'Export FastFlags',
            'Delete Profile'
        ]
        for i, option in enumerate(options, start=1):
            window.add_line(f'[{i}]: {option}')
        window.add_divider()
        
        bad_input: bool = False
        while True:
            response: str = window.get_input('Response: ')
            try:
                i = int(response)
                if i > 0 and i <= len(options):
                    bad_input = False
                    if i == 1:  # Go back
                        return
                    
                    elif i == 2:  # Toggle active state
                        fastflag_data.set(profile, not enabled, type='enabled')
                        break
                    
                    elif i == 3 or i == 4:  # Change name / description
                        window.add_line('Please choose a new name!' if i == 3 else 'Please choose a new description!')
                        window.add_divider()

                        bad_input = False
                        while True:
                            response: str = window.get_input('Response: ')

                            if i == 4:
                                fastflag_data.set(profile, response, type='description')
                                bad_input = False
                                raise Break
                            elif response not in [item.get('name', None) for item in fastflag_data.get_all()] or response == profile:
                                fastflag_data.set(profile, response, type='name')
                                profile = response
                                bad_input = False
                                raise Break

                            if bad_input != False:
                                window.remove_last(3)
                            
                            window.add_line(f'Invalid response: "{response}"')
                            window.add_line(f'Profile may not share the same name as another FastFlag profile!')
                            window.add_divider()
                            bad_input = True
                            window._on_update()
                    
                    elif i == 5:  # Add FastFlags
                        new_fastflag: dict = get_fastflag(window)
                        fastflag_data.set(profile, new_fastflag, type='data-add')
                        break
                    
                    elif i == 6:  # Remove FastFlags
                        window.add_line('Please type the name of the FastFlag you wish to remove! To cancel, type "cancel"')
                        window.add_divider()
                        bad_input = False
                        while True:
                            response: str = window.get_input('Response: ')

                            if response.lower() == 'cancel':
                                bad_input = False
                                raise Break

                            if response in fastflag_data.get(profile).get('data', None).keys():
                                fastflag_data.set(profile, response, type='data-remove')
                                bad_input = False
                                raise Break

                            if bad_input != False:
                                window.remove_last(3)
                            
                            window.add_line(f'Invalid response: "{response}"')
                            window.add_line(f'FastFlag not found!')
                            window.add_divider()
                            bad_input = True
                            window._on_update()
                    
                    elif i == 7:  # Import FastFlags
                        import_fastflags(window, profile)
                        break
                    
                    elif i == 8:  # Export FastFlags
                        export_fastflags(window, profile)
                        break
                    
                    elif i == 9:  # Delete profile
                        window.add_line('Are you sure? [Y/N]')
                        window.add_divider()

                        bad_input = False
                        while True:
                            response: str = window.get_input('Response: ')

                            if response.lower() in Response.CONFIRM:
                                fastflag_data.delete(profile)
                                bad_input = False
                                return
                            elif response.lower() in Response.DENY:
                                bad_input = False
                                raise Break

                            if bad_input != False:
                                window.remove_last(3)
                            
                            window.add_line(f'Invalid response: "{response}"')
                            window.add_line(f'Accepted answers are: [Y/N]')
                            window.add_divider()
                            bad_input = True
                            window._on_update()

        
            except Break as e:
                break

            except Exception as e:
                pass

            if bad_input != False:
                window.remove_last(3)
            window.add_line(f'Invalid response: "{response}"')
            window.add_line(f'Accepted answers are: [1-{len(options)}]')
            window.add_divider()
            bad_input = True
            window._on_update()


def get_fastflag(window: interface.Interface) -> dict:
    window.add_line('Enter the name of your FastFlag!')
    window.add_divider()

    fastflag_name: str = window.get_input('Response: ')
    window.remove_last(2)
    window.add_line(f'Enter a value for {fastflag_name}!')
    window.add_divider()
    fastflag_value: str = window.get_input('Response: ')

    fastflag: dict = {fastflag_name: fastflag_value}
    return fastflag


def import_fastflags(window: interface.Interface, profile: str) -> None:
    files = askopenfilenames(
                        filetypes=[('JSON files', '*.json')],
                        initialdir=os.path.join(os.getenv('HOME') or os.getenv('USERPROFILE'), 'Downloads'),
                        initialfile='ClientAppSettings.json',
                        title='Import FastFlags'
                    )
    
    try:

        if len(files) == 0:
            return
        
        else:
            for path in files:
                with open(path, 'r') as file:
                    data: dict = json.load(file)
                    file.close()
                    fastflag_data.set(profile, data, type='data-add')

    except Exception as e:
        window.add_line('Import failed!')
        window.add_line(f'An unexpected {type(e).__name__} occured: {str(e)}')
        window.add_divider()
        window.get_input('Press ENTER to return . . .')


def export_fastflags(window: interface.Interface, profile: str) -> None:
    target = asksaveasfilename(
                        filetypes=[('JSON files', '*.json')],
                        initialdir=os.path.join(os.getenv('HOME') or os.getenv('USERPROFILE'), 'Downloads'),
                        title='Export FastFlags'
                    )
    
    try:
        data: dict = fastflag_data.get(profile).get('data', {})

        with open(target, 'w') as file:
            json.dump(data, file, indent=4)
            file.close()

    except Exception as e:
        window.add_line('Export failed!')
        window.add_line(f'An unexpected {type(e).__name__} occured: {str(e)}')
        window.add_divider()
        window.get_input('Press ENTER to return . . .')