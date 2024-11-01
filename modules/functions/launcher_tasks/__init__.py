from .update import update
from .apply_mods import apply_mods
from .apply_fastflags import apply_fastflags
from .launch_roblox import launch_roblox


def apply_modifications(mods: list[str], version: str) -> None:
    apply_mods(mods, version)
    apply_fastflags(version)