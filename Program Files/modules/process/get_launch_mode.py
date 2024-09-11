import sys

from modules.other.launch_mode import MODLOADER_MENU, ROBLOX_PLAYER, ROBLOX_STUDIO, DEFAULT
from modules.utils import variables


def get_launch_mode() -> list[str]:
    args = sys.argv

    if len(args) == 1:
        return DEFAULT
    
    mode = args[1].lstrip('-')

    if len(args) > 2:
        variables.set('launch_arguments', ' '.join(args[2:]))

    if mode in MODLOADER_MENU:
        return MODLOADER_MENU
    
    elif mode in ROBLOX_PLAYER:
        return ROBLOX_PLAYER
    
    elif mode in ROBLOX_STUDIO:
        return ROBLOX_STUDIO
    
    return DEFAULT