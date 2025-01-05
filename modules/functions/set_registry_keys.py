import winreg
import sys

from modules.config import settings
from modules import Logger


IS_FROZEN = getattr(sys, "frozen", False)


def set_registry_keys() -> None:
    if not settings.get_value("set_registry_keys"):
        Logger.warning("Setting registry keys is disabled!")
        return
    
    if not IS_FROZEN:
        Logger.warning("Cannot set registry keys! Environment not frozen.")
        return
    
    Logger.info("Setting registry keys...")
    executable_path: str = sys.executable
    registry_keys: list[dict] = [
        {
            "key_name": r"roblox",
            "path": r"Software\Classes\roblox\shell\open\command",
            "value": rf"{executable_path} -l %1"
        },
        {
            "key_name": r"roblox-player",
            "path": r"Software\Classes\roblox-player\shell\open\command",
            "value": rf"{executable_path} -l %1"
        },
        {
            "key_name": r"roblox-studio",
            "path": r"Software\Classes\roblox-studio\shell\open\command",
            "value": rf"{executable_path} -s %1"
        }
    ]
    
    try:
        for item in registry_keys:
            key_name: str = item["key_name"]
            path: str = item["path"]
            value: str = item["value"]

            Logger.info(f"Setting {key_name} key...")
            key: winreg.HKEYType = winreg.CreateKey(winreg.HKEY_CURRENT_USER, path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, value)
            winreg.CloseKey(key)

    except Exception as e:
        Logger.error(f"Failed to set registry keys! {type(e).__name__}: {e}")