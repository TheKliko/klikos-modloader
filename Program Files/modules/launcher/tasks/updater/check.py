import os
from typing import Literal

from modules.filesystem import Directory
from modules.functions import latest_roblox_version, user_channel, settings


def check(binary_type: Literal["WindowsPlayer","WindowsStudio"], version: str|None = None, channel: str|None = None) -> bool:
    channel = channel or user_channel.get(binary_type=binary_type)
    version = version or latest_roblox_version.get(binary_type=binary_type, channel=channel)

    if settings.value("force_roblox_reinstallation", False) == True:
        settings.set("force_roblox_reinstallation", False)
        return True

    elif settings.value("always_update_roblox", False) == True:
        return True
    
    return not (
        os.path.isdir(os.path.join(
            Directory.versions(),
            version)
        ) and
        os.path.isfile(
            os.path.join(
                Directory.versions(),
                version,
                ("Roblox"+str("Player" if "player" in binary_type.lower() else "Studio")+"Beta.exe")
            )
        )
    )