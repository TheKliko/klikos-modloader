from modules import interface


def show(window) -> str:
    window.reset()
    window.add_line('Integrations', color=interface.Color.SECTION_TITLE)
    window.add_divider()

    raise NotImplementedError('Function not implemented!')

    next_section = window.get_input('Response: ')


    return next_section