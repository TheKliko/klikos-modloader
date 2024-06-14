import logging
import os
import winreg

from modules.utils import variables


def set_registry_key() -> None:
    # Postponed to v1.3.0 because I couldn't get it to launch from the website without giving an error 403 (authentication error)
    """Used to open Kliko's modloader when launching Roblox from the website"""
    logging.info('Setting registry key for Kliko\'s modloader')

    ROOT_DIRECTORY: str = variables.get('root_directory')
    REGISTRY_PATH: str = r'Software\Classes\roblox-player\shell\open\command'
    NEW_VALUE: str = f'"{ROOT_DIRECTORY}\Kliko\'s modloader.exe" %1'

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, NEW_VALUE)
        winreg.CloseKey(key)
    
    except Exception as e:
        logging.debug('Failed to set registry key!')
        logging.error(f'An unexpected {type(e).__name__} occured: {str(e)}')


def main() -> None:
    print(f'filename: {os.path.basename(__file__)}')
    print('description: module used in Kliko\'s modloader')
    print()
    input('Press ENTER to exit')


if __name__ == '__main__':
    main()