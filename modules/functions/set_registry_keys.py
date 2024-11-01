import winreg
import sys

from modules.logger import logger


IS_FROZEN = getattr(sys, "frozen", False)


def set_registry_keys() -> None:
    if not IS_FROZEN:
        return
    
    logger.info("Setting registry keys...")
    
    try:
        executable_path: str = sys.executable

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
        logger.error(f"{type(e).__name__}: {e}")
        logger.error("Failed to set registry keys!")