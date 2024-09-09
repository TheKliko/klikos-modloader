from modules import interface

from .. import mod_data


def show(window) -> str:
    while True:
        window.change_section_description()
        window.reset()

        try:
            mods: list[dict] = mod_data.get_all()
        except Exception as e:
            window.add_line('Section failed to load!', color=interface.Color.WARNING)
            window.add_line(f'[{type(e).__name__}]: {str(e)}', color=interface.Color.ERROR)
            window.add_divider()
            window.get_input('Press ENTER to return . . .')
            return 'home'


        options: list = [
            'Go Back'
        ] + [
            f'{interface.foreground(interface.Color.ON)}+{interface.Color.DEFAULT} {mod.get('name', 'ERROR_FAILED_TO_LOAD')}'
            if mod.get('enabled', False) == True
            else f'{interface.foreground(interface.Color.OFF)}-{interface.Color.DEFAULT} {mod.get('name', 'ERROR_FAILED_TO_LOAD')}'
            for mod in mods
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


def configure(window, mod: str) -> None:
    while True:
        window.change_section_description(f' > {mod}')
        window.reset()

        try:
            data: dict = mod_data.get(mod) 
        except Exception as e:
            window.add_line('Section failed to load!', color=interface.Color.WARNING)
            window.add_line(f'[{type(e).__name__}]: {str(e)}', color=interface.Color.ERROR)
            window.add_divider()
            window.get_input('Press ENTER to return . . .')
            return

        enabled: bool = data.get('enabled', False)
        priority: int = data.get('priority', 0)

        window.add_line(f'Name: {mod}')
        window.add_line(f'Status: {f'{interface.foreground(interface.Color.ON)}[enabled]{interface.Color.DEFAULT}' if enabled == True else f'{interface.foreground(interface.Color.OFF)}[disabled]{interface.Color.DEFAULT}'}')
        window.add_line(f'Load order: {priority}')
        window.add_line(' ')
        
        options: list = [
            'Go Back',
            'Toggle status',
            'Change load order'
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
                        mod_data.set(mod, not enabled)
                    
                    elif i == 3:
                        window.add_line('Please choose a new value!')
                        window.add_divider()
                        while True:
                            response: str = window.get_input('Response: ')

                            try:
                                i = int(response)
                                mod_data.set(mod, i)
                                bad_input = False
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