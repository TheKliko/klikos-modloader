from modules import interface

from .. import settings_data


def show(window: interface.Interface) -> str:
    while True:
        window.change_section_description()
        window.reset()

        try:
            data: dict = settings_data.get_all()
        except Exception as e:
            window.add_line('Section failed to load!', color=interface.Color.WARNING)
            window.add_line(f'[{type(e).__name__}]: {str(e)}', color=interface.Color.ERROR)
            window.add_divider()
            window.get_input('Press ENTER to return . . .')
            return 'home'


        options: list = [
            'Go Back'
        ] + [
            f'{interface.foreground(interface.Color.ON)}+{interface.Color.DEFAULT} {setting.get('name', 'ERROR_FAILED_TO_LOAD')}'
            if setting.get('value', False) == True
            else f'{interface.foreground(interface.Color.OFF)}-{interface.Color.DEFAULT} {setting.get('name', 'ERROR_FAILED_TO_LOAD')}'
            if setting.get('value', False) == True
            else f'{interface.foreground(interface.Color.WARNING)}{setting.get('value', 0)}{interface.Color.DEFAULT} {setting.get('name', 'ERROR_FAILED_TO_LOAD')}'
            for setting in data.values()
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
        
        configure(window, response)


def configure(window: interface.Interface, setting: str) -> None:
    while True:
        window.change_section_description(f' > {setting}')
        window.reset()

        try:
            data: dict = settings_data.get(setting) 
        except Exception as e:
            window.add_line('Section failed to load!', color=interface.Color.WARNING)
            window.add_line(f'[{type(e).__name__}]: {str(e)}', color=interface.Color.ERROR)
            window.add_divider()
            window.get_input('Press ENTER to return . . .')
            return

        setting_type: str = data.get('type', False)
        value: bool = data.get('value', False)
        default: bool = data.get('default', False)
        description: int = data.get('description', None)
        range: dict = data.get('range', None)

        window.add_line(f'Setting: {setting}')
        window.add_line(f'Description: {description}')
        window.add_line(f'Type: {setting_type}')

        if setting_type == 'bool':
            window.add_line(f'Default: {'Enabled' if default == True else 'Disabled'}')
            window.add_line(f'Status: {f'{interface.foreground(interface.Color.ON)}[enabled]{interface.Color.DEFAULT}' if value == True else f'{interface.foreground(interface.Color.OFF)}[disabled]{interface.Color.DEFAULT}'}')
        else:
            window.add_line(f'Default: {default}')
            window.add_line(f'Value: {interface.foreground(interface.Color.WARNING)}{value}{interface.Color.DEFAULT}')
        if range is not None and setting_type == 'int':
            window.add_line(f'Range: [{range.get('min', None) or '-Any'}-{range.get('max', None) or 'Any'}]')
        window.add_line(' ')
        
        options: list = [
            'Go Back',
            'Toggle status' if setting_type == 'bool' else 'Change value',
            'Reset to default'
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
                    if i == 1:
                        return
                    
                    elif i == 2:
                        if setting_type == 'bool':
                            settings_data.set(setting, not value)

                        elif setting_type == 'int':
                            window.add_line('Please choose a new value!')
                            window.add_divider()
                            while True:
                                response: str = window.get_input('Response: ')

                                try:
                                    min: int = range.get('min', None)
                                    max: int = range.get('max', None)
                                    i = int(response)
                                    if ((min is not None and i >= min) or min is None) and ((max is not None and i <= max) or max is None):
                                        settings_data.set(setting, i)
                                        bad_input = False
                                        break
                                except:
                                    pass

                                if bad_input != False:
                                    window.remove_last(3)
                                
                                window.add_line(f'Invalid response: "{response}"')
                                window.add_line(f'Accepted answers are: [{range.get('min', None) or '-Any'}-{range.get('max', None) or 'Any'}]')
                                window.add_divider()
                                bad_input = True
                                window._on_update()
                    
                    elif i == 3:
                        settings_data.set(setting, default)
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