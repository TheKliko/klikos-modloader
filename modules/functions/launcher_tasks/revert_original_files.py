import os
from typing import Literal

from modules.logger import logger
from modules.filesystem import Directory, extract, logged_path


def revert_original_files(version: str, mode: Literal["WindowsPlayer", "WindowsStudio"]) -> None:
    logger.info("Reverting original files...")

    downloads: str = Directory.downloads_player() if mode == "WindowsPlayer" else Directory.downloads_studio()
    source: str = os.path.join(downloads, f"{version}.zip")
    target: str = os.path.join(Directory.versions(), version)

    if not os.path.isfile(source):
        logger.warning(f"Failed to revert original files: {logged_path.get(source)} not found!")
    
    extract(source, target)