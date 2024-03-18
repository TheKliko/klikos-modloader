# Modloader.py
# Roblox modloader made by Kliko

from Functions import display_countdown_message, get_roblox_version, update_json_settings, read_json_settings, get_directories_from_folder, remove_sub_directories, copy_directory, launch_application, select_item_from_list
import os
import sys

modloader_version: str = '2.1'
launcher_args: str = '-Launcher'
setup_args: str = '-Setup'
info_args: str = '-Info'
main_directory: str = os.path.join(str(os.getenv('LOCALAPPDATA')), 'Roblox modloader')
mods_directory: str = os.path.join(main_directory, 'Mods')
fastflags_directory: str = os.path.join(main_directory, r'FastFlags\ClientSettings')
json_directory: str = os.path.join(main_directory, r'Files\Settings.json')
version_directory: str  = os.path.join(main_directory, 'Version folder')

current_version = read_json_settings(path=json_directory, name='CurrentVersion')
current_mod = read_json_settings(path=json_directory, name='CurrentMod')
fastflags_state = read_json_settings(path=json_directory, name='FastFlags')



def run_launch_process():
    launch_application(path=os.path.join(version_directory, current_version, 'RobloxPlayerBeta.exe'), name='Roblox')

def run_setup_process():
    version_name, roblox_directory = get_roblox_version()
    print('Resetting Version folder...')
    remove_sub_directories(version_directory)
    copy_directory(path1=roblox_directory, path2=os.path.join(version_directory, version_name))
    update_json_settings(path=json_directory, name='CurrentVersion', value=version_name)
    update_json_settings(path=json_directory, name='CurrentMod', value='Unmodded')
    update_json_settings(path=json_directory, name='FastFlags', value=False)

    print('Looking for mods...')
    installed_mods = get_directories_from_folder(path=mods_directory)
    installed_mods.insert(0, 'Unmodded')
    print('Found the following mods:')
    mod_name = select_item_from_list(list=installed_mods)
    if mod_name == 'Unmodded':
        update_json_settings(path=json_directory, name='CurrentMod', value=mod_name)
        print('No mods applied.')
    else:
        print(f'Applying the following mod: {mod_name}')
        copy_directory(path1=os.path.join(mods_directory, mod_name), path2=os.path.join(version_directory, version_name))
        update_json_settings(path=json_directory, name='CurrentMod', value=mod_name)

    print('Looking for FastFlags...')
    if os.path.exists(fastflags_directory):
        print('FastFlags found, do you wish to apply? [Y/N]')
        while True:
            fastflags_preference = input('\nResponse: ').lower()
            if fastflags_preference in ['yes','y']:
                print('Applying FastFlags...')
                copy_directory(path1=fastflags_directory, path2=os.path.join(version_directory, version_name, 'ClientSettings'))
                update_json_settings(path=json_directory, name='FastFlags', value=True)
                break
            elif fastflags_preference in ['no','n']:
                update_json_settings(path=json_directory, name='FastFlags', value=False)
                break
            else:
                print('ERROR: Invalid choice!\n')
    else:
        print('No FastFlags found.')
    print('All tasks completed!')

def run_info_process():
    print(f'Modloader version: {modloader_version}')
    print(f'Roblox version: {current_version}')
    print(f'Current mod: {current_mod}')
    print(f'FastFlags: {fastflags_state}\n')
    input(f'Press ENTER to exit')



def main():
    # print(f'You are currently using Kliko\'s modloader version {modloader_version}\n')

    if not len(sys.argv) > 1:
        print("ERROR: Unspecified launch arguments")
    elif sys.argv[1] != setup_args and sys.argv[1] != launcher_args and sys.argv[1] != info_args:
        print("ERROR: Unknown launch arguments")
    elif sys.argv[1] == launcher_args:
        run_launch_process()
    elif sys.argv[1] == setup_args:
        run_setup_process()
    elif sys.argv[1] == info_args:
        run_info_process()

    display_countdown_message(message='Terminating process', duration=3)

if __name__ == '__main__':
    main()