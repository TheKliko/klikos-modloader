import logging
import os
import time
from PIL import Image

from modules.other.paths import Directory


def get_modded_icons(
        mods: list[str],
        imageset_paths: list[dict[str,str]],
        icon_maps: dict[str,dict[str,dict[str,str|int]]],
        studio_version: str,
        temp_directory: str
    ) -> dict[str,dict[str,list]]:

    logging.info('Getting modded icons . . .')
    icon_map: dict = icon_maps[studio_version]
    modded_icons: dict = {}
    path_to_unmodded_imagesets: str = os.path.join(
        temp_directory,
        studio_version,
        [path['path'] for path in imageset_paths if path['version'] == studio_version][0]
    )
    
    for mod in mods:
        modded_icons[mod] = {
            '1x': [],
            '2x': [],
            '3x': []
        }

        base_path: str = os.path.join(Directory.MODS, mod)
        path_to_mod_imagesets: str = None
        for dirpath, dirnames, filenames in os.walk(base_path):
            for file in filenames:
                if file.startswith('img_set'):
                    path_to_mod_imagesets: str = dirpath
                    break
            if path_to_mod_imagesets != None:
                break
        else:
            raise Exception('[mod_updater.get_modded_icons] ImageSets not found!')

        for size, icons in icon_map.items():
            for name in list(icons.keys()):
                imageset: str = icon_map[size][name]['set']
                x: int = icon_map[size][name]['x']
                y: int = icon_map[size][name]['y']
                w: int = icon_map[size][name]['w']
                h: int = icon_map[size][name]['h']

                path_1: str = os.path.join(path_to_mod_imagesets, f'{imageset}.png')
                path_2: str = os.path.join(path_to_unmodded_imagesets, f'{imageset}.png')

                if not os.path.isfile(path_1):
                    continue

                if not os.path.isfile(path_2):
                    raise Exception(f'Could not find {os.path.basename(path_2)}')

                icon_1: Image.Image = Image.open(path_1).crop((x,y,x+w,y+h))
                icon_2: Image.Image = Image.open(path_2).crop((x,y,x+w,y+h))

                if not is_same_icon(icon_1, icon_2):
                    # print(f'Modded icon detected: {size}/{name}')
                    modded_icons[mod][size].append(name)

                    # preview_image: Image.Image = Image.new('RGBA', (w*2, h))
                    # preview_image.paste(icon_1, (0,0))
                    # preview_image.paste(icon_2, (w, 0))
                    # print(f'icon preview: {name}')
                    # preview(preview_image)

    return modded_icons


def is_same_icon(icon1: Image.Image, icon2: Image.Image) -> bool:
    if icon1.mode != icon2.mode or icon1.size != icon2.size:
        return False
    
    data1 = icon1.load()
    data2 = icon2.load()

    for x in range(icon1.width):
        for y in range(icon1.height):
            if data1[x, y] != data2[x, y]:
                if icon1.mode == 'RGBA':
                    if data1[x,y][3] == 0 and data2[x,y][3] == 0:
                        continue
                return False
    
    return True


# Used for debugging
def preview(image: Image.Image) -> None:
    if isinstance(image, Image.Image):
        image.show()
        time.sleep(2)
        os.system("taskkill /f /im Photos.exe >nul 2>&1")
    
    else:
        print('Unable to preview image')