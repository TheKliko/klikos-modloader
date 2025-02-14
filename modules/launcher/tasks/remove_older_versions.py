from pathlib import Path
import shutil

from modules import Logger
from modules.filesystem import Directory


def remove_older_versions(player_version: str, studio_version: str) -> None:
    current_versions: list[str] = [player_version, studio_version]

    if Directory.VERSIONS.is_dir():
        for directory in Directory.VERSIONS.iterdir():

            if not directory.is_dir():
                continue

            if directory.name not in current_versions:
                Logger.info(f"Removing older Roblox version: {directory.name}")
                try:
                    shutil.rmtree(directory)
                except Exception as e:
                    Logger.warning(f"Failed to remove {directory.name}! {type(e).__name__}: {e}")