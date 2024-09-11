import logging
import os
import shutil
from PIL import Image

from modules.other.paths import Directory


def generate_imagesets(
        modded_icons: dict[str,dict[str,list]],
        imageset_paths: list[dict[str,str]],
        icon_maps: dict[str,dict[str,dict[str,str|int]]],
        mod_studio_version: str,
        latest_studio_version: str,
        temp_directory: str
    ) -> None:

    logging.info('Generating ImageSets . . .')
    icon_map_old: dict = icon_maps[mod_studio_version]
    icon_map_new: dict = icon_maps[latest_studio_version]
    path_to_unmodded_imagesets: str = os.path.join(
        temp_directory,
        latest_studio_version,
        [path['path'] for path in imageset_paths if path['version'] == latest_studio_version][0]
    )

    for mod in modded_icons.keys():
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

        path_to_updated_imagesets: str = os.path.join(
            temp_directory,
            mod,
            [path['path'] for path in imageset_paths if path['version'] == latest_studio_version][0]
        )

        shutil.copytree(path_to_unmodded_imagesets, path_to_updated_imagesets)

        used_imagesets: list[str] = []
        for size, icons in modded_icons[mod].items():
            for name in icons:
                icon_data: dict = icon_map_old[size][name]
                imageset: str = icon_data['set']
                icon_path: str = os.path.join(path_to_mod_imagesets, f'{imageset}.png')

                x: int = icon_data['x']
                y: int = icon_data['y']
                w: int = icon_data['w']
                h: int = icon_data['h']

                icon: Image.Image = Image.open(icon_path)
                icon = icon.crop((x,y,x+w,y+h))
                
                new_icon_data = icon_map_new[size][name]
                imageset: str = new_icon_data['set']
                x: int = new_icon_data['x']
                y: int = new_icon_data['y']
                image: Image.Image = Image.open(os.path.join(path_to_updated_imagesets, f'{imageset}.png'))
                image.paste(icon, (x,y))
                image.save(os.path.join(path_to_updated_imagesets, f'{imageset}.png'))

                if imageset not in used_imagesets:
                    used_imagesets.append(f'{imageset}.png')
        
        delete_unmodded_imagesets(path_to_updated_imagesets, used_imagesets)


# Prevents bloat from unmodded files
def delete_unmodded_imagesets(savepath, used_imagesets):
    imagesets: list[str] = os.listdir(savepath)
    to_be_deleted: list[str] = [file for file in imagesets if not file in used_imagesets]
    for file in to_be_deleted:
        path: str = os.path.join(savepath, file)
        os.remove(path)