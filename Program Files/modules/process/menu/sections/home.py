from modules import interface


def show(window) -> str:
    window.reset()

    options: list[dict[str,str|list[str]]] = [
        {
            'name': 'Exit',
            'alias': ['exit', 'quit', 'close'],
            'value': 'exit'
        },
        {
            'name': 'Mods',
            'alias': [
                'mods',
                'mod',
                'm'
            ],
            'value': 'mods'
        },
        {
            'name': 'FastFlags',
            'alias': [
                'fastflags',
                'fastflag',
                'fflags',
                'fflag',
                'flags',
                'flag',
                'f'
            ],
            'value': 'fastflags'
        },
        {
            'name': 'Marketplace',
            'alias': [
                'marketplace',
                'market',
                'workshop',
                'community mods',
                'community',
                'rmc'
            ],
            'value': 'marketplace'
        },
        {
            'name': 'Integrations',
            'alias': [
                'integrations',
                'i'
            ],
            'value': 'integrations'
        },
        {
            'name': 'Settings',
            'alias': [
                'settings',
                's'
            ],
            'value': 'settings'
        },
        {
            'name': 'About',
            'alias': [
                'about',
                'info'
            ],
            'value': 'about'
        }
    ]

    for i, item in enumerate([option.get('name', 'ERROR_BAD_VALUE') for option in options], start=1):
        window.add_line(f'[{i}]: {item}')
    window.add_divider()

    bad_input: bool = False
    while True:
        response = window.get_input('Response: ')
        try:
            i = int(response)
            if i > 0 and i <= len(options):
                next_section = options[i-1]['value']
                break
        except:
            pass

        try:
            for item in options:
                if response in item.get('alias', []):
                    next_section = item['value']
                    break
        except:
            pass

        if bad_input == False:
            window.add_line(f'Invalid response: "{response}"')
            window.add_line(f'Accepted answers are: [1-{len(options)}]')
            window.add_divider()
        bad_input = True

    return next_section