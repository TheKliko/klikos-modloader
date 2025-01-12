import sys
import platform

from modules.config import settings
from modules import Logger


IS_FROZEN = getattr(sys, "frozen", False)


def set_registry_keys() -> None:
    if not settings.get_value("set_registry_keys"):
        Logger.warning("Setting registry keys is disabled!")
        return
    
    if platform.system() != "Windows":
        Logger.warning("Cannot set registry keys! User is not on Windows.")
        return
    
    if not IS_FROZEN:
        Logger.warning("Cannot set registry keys! Environment not frozen.")
        return
    
    import winreg
    
    Logger.info("Setting registry keys...")
    executable_path: str = sys.executable
    registry_keys: dict[str, list[dict[str, str]]] = {
        "roblox": [
            {
                "path": r"Software\Classes\roblox",
                "value": r"URL: Roblox Protocol"
            },
            {
                "path": r"Software\Classes\roblox",
                "key": r"URL Protocol",
                "value": r""
            },
            {
                "path": r"Software\Classes\roblox\DefaultIcon",
                "value": rf'"{executable_path}"'
            },
            {
                "path": r"Software\Classes\roblox\shell\open\command",
                "value": rf'"{executable_path}" -l %1'
            },
        ],
        "roblox-player": [
            {
                "path": r"Software\Classes\roblox-player",
                "value": r"URL: Roblox Protocol"
            },
            {
                "path": r"Software\Classes\roblox-player",
                "key": r"URL Protocol",
                "value": r""
            },
            {
                "path": r"Software\Classes\roblox-player\DefaultIcon",
                "value": rf'"{executable_path}"'
            },
            {
                "path": r"Software\Classes\roblox-player\shell\open\command",
                "value": rf'"{executable_path}" -l %1'
            },
        ],
        "roblox-studio": [
            {
                "path": r"Software\Classes\roblox-studio",
                "value": r"URL: Roblox Protocol"
            },
            {
                "path": r"Software\Classes\roblox-studio",
                "key": r"URL Protocol",
                "value": r""
            },
            {
                "path": r"Software\Classes\roblox-studio\DefaultIcon",
                "value": rf'"{executable_path}"'
            },
            {
                "path": r"Software\Classes\roblox-studio\shell\open\command",
                "value": rf'"{executable_path}" -s %1'
            },
        ],
        "Roblox.Place": [
            {
                "path": r"Software\Classes\Roblox.Place",
                "value": r"Roblox Place"
            },
            {
                "path": r"Software\Classes\Roblox.Place\DefaultIcon",
                "value": rf'"{executable_path}"'
            },
            {
                "path": r"Software\Classes\Roblox.Place\shell\Open",
                "value": r"Open"
            },
            {
                "path": r"Software\Classes\Roblox.Place\shell\Open\command",
                "value": rf'"{executable_path}" -s %1'
            }
        ],
        "roblox-studio-auth": [
            {
                "path": r"Software\Classes\roblox-studio-auth",
                "value": r"URL: Roblox Protocol"
            },
            {
                "path": r"Software\Classes\roblox-studio-auth",
                "key": r"URL Protocol",
                "value": r""
            },
            {
                "path": r"Software\Classes\roblox-studio-auth\DefaultIcon",
                "value": rf'"{executable_path}"'
            },
            {
                "path": r"Software\Classes\roblox-studio-auth\shell\open\command",
                "value": rf'"{executable_path}" -s %1'
            },
        ]
    }

    for group, keys in registry_keys.items():
        Logger.info(f"Setting registry keys for {group}...")
        for item in keys:
            path: str = item["path"]
            key_name: str = item.get("key", "")
            value: str = item["value"]

            try:
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, path) as key:
                    winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, value)

            except Exception as e:
                Logger.warning(f"Failed to set registry key for {path}! {type(e).__name__}: {e}")