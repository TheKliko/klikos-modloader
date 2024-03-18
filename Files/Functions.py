# Functions.py
# Module used in Kliko's modloader

import time
import os
import requests as request
import json
import shutil
import subprocess



def display_countdown_message(message: str, duration: int) -> None:
    format_string = '{:<'+str(len(message+' in '+str(duration)))+'}'
    for i in range(duration)[::-1]:
        print(format_string.format(f'{message} in {i+1}'), end='\r')
        time.sleep(1)
    print(format_string.format(f'{message} now...'))
    time.sleep(1)

def get_roblox_version() -> tuple | None:
    for i in range(0,5):
            version_name = [x for x in [x for x in request.get("https://setup.rbxcdn.com/DeployHistory.txt").text.split('\n') if x.startswith('New WindowsPlayer')][-i].split(' ') if x.startswith('version-')][0]
            version_directory = str(os.getenv('LOCALAPPDATA')) + r"\Roblox\Versions" + '\\' + version_name
            check1 = os.path.exists(version_directory)
            if check1:
                return (version_name, version_directory)
    print('ERROR: Failed to find latest Roblox version')
    return None

def read_json_settings(path: str, name: str) -> str | int | bool | None:
    try:
        with open(path, 'r+') as file:
            config = json.load(file)
            return config[name]
    except:
        print('ERROR: Failed to read Settings.json')
        return None

def update_json_settings(path: str, name: str, value: str | int | bool) -> None:
    try:
        with open(path, 'r+') as file:
            config = json.load(file)
            config[name] = value
            file.seek(0)
            json.dump(config, file)
            file.truncate()
    except:
        print('ERROR: Failed to update Settings.json')

def get_directories_from_folder(path: str) -> list:
    directories = []
    for directory in os.listdir(path):
        directories.append(directory)
    return directories

def remove_directory(path: str) -> None:
    try:
        shutil.rmtree(path)
    except:
        print(f'ERROR: Failed to delete {path}')

def remove_sub_directories(path: str) -> None:
    for root, dirs, files in os.walk(path):
        if root != path:
            remove_directory(path=root)

def copy_directory(path1: str, path2: str) -> None:
    try:
        shutil.copytree(path1, path2, dirs_exist_ok=True)
    except:
        print(f'ERROR: Failed to copy {path1} to {path2}')

def launch_application(path: str, name: str) -> None:
    try:
        print(f'Launching {name}... Please wait')
        subprocess.run(path)
    except:
        pass
        print(f'ERROR: Failed to launch {name}')

def select_item_from_list(list) -> str:
    while True:
        try:
            for i in list:
                print(f'[{list.index(i)}]: {i}')
            selected = int(input('\nMake your choice: '))
            if list[selected] in list:
                break
        except:
            print('ERROR: Invalid choice')
            print('Please make sure that you enter the number corresponding to the item you wish to select\n')
    return list[selected]



def main():
    input('Functions.py\nModule used in Kliko\'s modloader')

if __name__ == '__main__':
    main()