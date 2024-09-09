import logging

from modules.interface import interface

from .sections import home, mods, fastflags, integrations, settings, about, marketplace
from . import integrations_data, settings_data


def run() -> None:
    logging.info(f'Sarting modloader menu . . .')

    menu: Window = Window()


class Window:
    window: interface.Interface = None

    def __init__(self) -> None:
        self._home()

    def _home(self) -> None:
        self.window = interface.Interface(section='Modloader Menu - Home')
        self.active_section = home.show(self.window)
        self._on_update()

    def _mods(self) -> None:
        self.window = interface.Interface(section='Modloader Menu - Mods')
        self.active_section = mods.show(self.window)
        self._on_update()

    def _fastflags(self) -> None:
        self.window = interface.Interface(section='Modloader Menu - FastFlags')
        self.active_section = fastflags.show(self.window)
        self._on_update()

    def _marketplace(self) -> None:
        self.window = interface.Interface(section='Modloader Menu - Marketplace')
        self.active_section = marketplace.show(self.window)
        self._on_update()

    def _integrations(self) -> None:
        self.window = interface.Interface(section='Modloader Menu - Integrations')
        self.active_section = integrations.show(self.window)
        self._on_update()

    def _settings(self) -> None:
        self.window = interface.Interface(section='Modloader Menu - Settings')
        self.active_section = settings.show(self.window)
        self._on_update()

    def _about(self) -> None:
        self.window = interface.Interface(section='Modloader Menu - About')
        self.active_section = about.show(self.window)
        self._on_update()

    def _on_update(self) -> None:
        section: str = self.active_section

        if section == 'exit':
            return

        elif section == 'home':
            self._home()

        elif section == 'mods':
            self._mods()

        elif section == 'fastflags':
            self._fastflags()

        elif section == 'marketplace':
            self._marketplace()

        elif section == 'integrations':
            self._integrations()

        elif section == 'settings':
            self._settings()

        elif section == 'about':
            self._about()

        self.window._on_update()