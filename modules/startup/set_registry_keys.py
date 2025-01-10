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
            "identifier": r"roblox_shell-command",
            "path": r"Software\Classes\roblox\shell\open\command",
            "value": rf'"{executable_path}" -l %1'
        },
        {
            "identifier": r"roblox-player_shell-command",
            "path": r"Software\Classes\roblox-player\shell\open\command",
            "value": rf'"{executable_path}" -l %1'
        },
        {
            "identifier": r"roblox-studio_shell-command",
            "path": r"Software\Classes\roblox-studio\shell\open\command",
            "value": rf'"{executable_path}" -s %1'
        },
        {
            "identifier": r"roblox_default",
            "path": r"Software\Classes\roblox",
            "value": r"URL: Roblox Protocol"
        },
        {
            "identifier": r"roblox-player_default",
            "path": r"Software\Classes\roblox-player",
            "value": r"URL: Roblox Protocol"
        },
        {
            "identifier": r"roblox-studio_default",
            "path": r"Software\Classes\roblox-studio",
            "value": r"URL: Roblox Protocol"
        },
        {
            "identifier": r"roblox_url-protocol",
            "path": r"Software\Classes\roblox",
            "key": r"URL Protocol",
            "value": r""
        },
        {
            "identifier": r"roblox-player_url-protocol",
            "path": r"Software\Classes\roblox-player",
            "key": r"URL Protocol",
            "value": r""
        },
        {
            "identifier": r"roblox-studio_url-protocol",
            "path": r"Software\Classes\roblox-studio",
            "key": r"URL Protocol",
            "value": r""
        }
    ]

    for item in registry_keys:
        try:
            identifier: str = item["identifier"]
            path: str = item["path"]
            key_name: str | None = item.get("key")
            value: str = item["value"]

            Logger.info(f"Setting {identifier} key...")
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, path) as key:
                if key_name is None:
                    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, value)
                else:
                    winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, value)

        except Exception as e:
            Logger.error(f"Failed to set registry key! {type(e).__name__}: {e}")