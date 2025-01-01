from typing import Literal

from modules.functions.config import settings

from .update import update
from .revert_original_files import revert_original_files
from .apply_mods import apply_mods
from .apply_fastflags import apply_fastflags
from .launch_roblox import launch_roblox
from .wait_until_roblox_is_launched import wait_until_roblox_is_launched
from .run_launch_apps import run_launch_apps


def apply_modifications(mods: list[str], version: str, mode: Literal["WindowsPlayer", "WindowsStudio"], skip_file_restore: bool = False) -> None:
    if skip_file_restore is not True:
        revert_original_files(version, mode)

    if settings.value("disable_all_mods") is not True:
        apply_mods(mods, version)
        
    if settings.value("disable_all_fastflags") is not True:
        apply_fastflags(version)