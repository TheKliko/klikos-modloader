import logging
import os
import winreg

from modules.utils import variables


def set_registry_keys() -> None:
    logging.info('Setting registry keys . . .')

    root: str = variables.get('root')
    path_to_executable: str = os.path.join(root, 'kliko\'s modloader.exe')

    registry_path: str = r'Software\Classes\roblox\shell\open\command'
    roblox_player_registry_path: str = r'Software\Classes\roblox-player\shell\open\command'
    roblox_studio_registry_path: str = r'Software\Classes\roblox-studio\shell\open\command'

    roblox_player_value: str = rf'"{path_to_executable}" -l %1'
    roblox_studio_value: str = rf'"{path_to_executable}" -s %1'

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, roblox_player_value)
        winreg.CloseKey(key)
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, roblox_player_registry_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, roblox_player_value)
        winreg.CloseKey(key)
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, roblox_studio_registry_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, roblox_studio_value)
        winreg.CloseKey(key)
    
    except Exception as e:
        logging.error('Failed to set registry keys!')
        logging.error(f'[{type(e).__name__}] {str(e)}')