import json
import os
import shutil

from modules.other.paths import Directory


def update_mods(mods: list[str], temp_directory: str, latest_version: str) -> None:
    for mod in mods:
        source: str = os.path.join(temp_directory, mod)
        target: str = os.path.join(Directory.MODS, mod)

        base_path: str = os.path.join(Directory.MODS, mod)
        path_to_mod_imagesets: str = None
        for dirpath, dirnames, filenames in os.walk(base_path):
            for filename in filenames:
                if filename.startswith('img_set'):
                    path_to_mod_imagesets: str = dirpath
                    break
            if path_to_mod_imagesets != None:
                break

        shutil.rmtree(path_to_mod_imagesets, ignore_errors=True)
        path: str = path_to_mod_imagesets
        while True:
            path = os.path.dirname(path)
            if os.listdir(path) != []:
                break
            shutil.rmtree(path)

        shutil.copytree(source, target, dirs_exist_ok=True)

        with open(os.path.join(target, 'info.json'), 'r') as file:
            data: dict = json.load(file)
            file.close()

        data['clientVersionUpload'] = latest_version

        with open(os.path.join(target, 'info.json'), 'w') as file:
            json.dump(data, file)
            file.close()