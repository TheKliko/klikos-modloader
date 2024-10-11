import logging
import os
import winreg

from modules.filesystem import Directory


def set() -> None:
    try:
        root: str = Directory.root()
        executable_path: str = os.path.join(root, "Kliko's modloader.exe")

        registry_path: str = r"Software\Classes\roblox\shell\open\command"
        roblox_player_registry_path: str = r"Software\Classes\roblox-player\shell\open\command"
        roblox_studio_registry_path: str = r"Software\Classes\roblox-studio\shell\open\command"

        roblox_player_value: str = executable_path+" -l %1"
        roblox_studio_value: str = executable_path+" -s %1"

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, roblox_player_value)
        winreg.CloseKey(key)
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, roblox_player_registry_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, roblox_player_value)
        winreg.CloseKey(key)
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, roblox_studio_registry_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, roblox_studio_value)
        winreg.CloseKey(key)

    except Exception as e:
        logging.warning("Failed to set registry keys!")
        logging.warning(type(e).__name__+": "+str(e))