import logging
import os
import tempfile
import webbrowser

from modules import interface
from modules.other.api import Api
from modules.other.paths import Directory
from modules.utils import filesystem

from .. import marketplace_data


def show(window: interface.Interface) -> str:
    while True:
        window.change_section_description()
        window.reset()

        try:
            data: list[dict[str,str]] = marketplace_data.get_all()
        except Exception as e:
            window.add_line('Section failed to load!', color=interface.Color.WARNING)
            window.add_line(f'[{type(e).__name__}]: {str(e)}', color=interface.Color.ERROR)
            window.add_divider()
            window.get_input('Press ENTER to return . . .')
            return 'home'


        options: list = [
            'Go Back'
        ] + [
            item.get('name', 'BAD_DATA') for item in data
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
                    mod: dict[str,str] = [item for item in data if item.get('name', None) == options[i-1]][0]
                    # options[i-1]
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

        more_info(window, mod)


def more_info(window: interface.Interface, data: dict[str,str]) -> None:
    while True:
        name: str = data.get('name', None)
        creator: str = data.get('creator', None) or data.get('author', None) or 'UNKNOWN'
        description: str = data.get('description', None)
        id: str = data.get('id', 'BAD_DATA')
        preview: str = data.get('preview', None)

        window.change_section_description(f' > {name}')
        window.reset()

        window.add_line(f'Name: {name}')
        window.add_line(f'Made by: {creator}')
        window.add_line(f'Description: {description}')
        window.add_line(f'ID: {id}')
        window.add_line(' ')
        
        options: list = [
            'Go Back',
            'Download Mod'
        ]
        if preview is not None:
            options.append('Show Preview (web browser)')
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
                        download_mod(window, mod_id=id, mod_name=name)
                    
                    elif i == 3:
                        webbrowser.open(preview, new=2)
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


def download_mod(window: interface.Interface, mod_id, mod_name) -> None:
    try:
        with tempfile.TemporaryDirectory() as temp_directory:
            logging.info(f'Downloading mod: "{mod_id}"')
            url: str = Api.marketplace(mod_id)
            download_target: str = os.path.join(temp_directory, f'{mod_id}.zip')
            target: str = os.path.join(Directory.MODS, mod_name)

            window.add_line(f'Downloading mod: "{mod_name}" . . .', color=interface.Color.WARNING)
            window.add_divider()
            filesystem.download(url, download_target)

            window.remove_last()
            window.add_line(f'Extracting mod: "{mod_name}" . . .', color=interface.Color.WARNING)
            window.add_divider()
            filesystem.extract(download_target, target)

            window.remove_last()
            window.add_line(f'Mod download success!', color=interface.Color.ON)
            window.add_divider()
            window.get_input('Press ENTER to return . . .')

    except Exception as e:
        window.add_line('\u26a0  Mod download failed!', color=interface.Color.WARNING)
        window.add_line(f'{type(e).__name__}: {str(e)}', color=interface.Color.ERROR)
        window.add_divider()
        window.get_input('Press ENTER to return . . .')