import logging
import os
import winreg

from modules.utils import variables


def set_registry_key() -> None:
    """Used to open Kliko's modloader when launching Roblox from the website"""
    logging.info('Setting registry key for Kliko\'s modloader')

    ROOT: str = variables.get('root')
    REGISTRY_PATH: str = r'Software\Classes\roblox-player\shell\open\command'
    STUDIO_REGISTRY_PATH: str = r'Software\Classes\roblox-studio\shell\open\command'
    NEW_VALUE: str = f'"{ROOT}\Kliko\'s modloader.exe" -play %1'
    STUDIO_NEW_VALUE: str = f'"{ROOT}\Kliko\'s modloader.exe" -studio %1'

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, NEW_VALUE)
        winreg.CloseKey(key)
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STUDIO_REGISTRY_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, STUDIO_NEW_VALUE)
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