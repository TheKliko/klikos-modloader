from modules import interface

from .. import integrations_data


def show(window: interface.Interface) -> str:
    while True:
        window.change_section_description()
        window.reset()

        try:
            data: dict = integrations_data.get_all()
        except Exception as e:
            window.add_line('Section failed to load!', color=interface.Color.WARNING)
            window.add_line(f'[{type(e).__name__}]: {str(e)}', color=interface.Color.ERROR)
            window.add_divider()
            window.get_input('Press ENTER to return . . .')
            return 'home'


        options: list = [
            'Go Back'
        ] + [
            f'{interface.foreground(interface.Color.ON)}+{interface.Color.DEFAULT} {integration.get('name', 'ERROR_FAILED_TO_LOAD')}'
            if integration.get('value', False) == True
            else f'{interface.foreground(interface.Color.OFF)}-{interface.Color.DEFAULT} {integration.get('name', 'ERROR_FAILED_TO_LOAD')}'
            for integration in data.values()
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


def configure(window: interface.Interface, integration: str) -> None:
    while True:
        window.change_section_description(f' > {integration}')
        window.reset()

        try:
            data: dict = integrations_data.get(integration) 
        except Exception as e:
            window.add_line('Section failed to load!', color=interface.Color.WARNING)
            window.add_line(f'[{type(e).__name__}]: {str(e)}', color=interface.Color.ERROR)
            window.add_divider()
            window.get_input('Press ENTER to return . . .')
            return

        enabled: bool = data.get('value', False)
        default: bool = data.get('default', False)
        description: int = data.get('description', None)
        dependencies: int = data.get('dependencies', None)
        dependants: int = data.get('dependants', None)

        window.add_line(f'Integration: {integration}')
        window.add_line(f'Description: {description}')
        window.add_line(f'Default: {'Enabled' if default == True else 'Disabled'}')
        window.add_line(f'Status: {f'{interface.foreground(interface.Color.ON)}[enabled]{interface.Color.DEFAULT}' if enabled == True else f'{interface.foreground(interface.Color.OFF)}[disabled]{interface.Color.DEFAULT}'}')
        if dependencies is not None:
            window.add_line(f'Dependencies: {', '.join([f'{interface.foreground(interface.Color.WARNING)}{dependency.get('setting', 'ERROR')}{interface.Color.DEFAULT}' for dependency in dependencies])}')
        if dependants is not None:
            window.add_line(f'Dependants: {', '.join([f'{interface.foreground(interface.Color.WARNING)}{dependant}{interface.Color.DEFAULT}' for dependant in dependants])}')
        window.add_line(' ')
        
        options: list = [
            'Go Back',
            'Toggle status',
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
                        integrations_data.set(integration, not enabled)
                    
                    elif i == 3:
                        integrations_data.set(integration, default)
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