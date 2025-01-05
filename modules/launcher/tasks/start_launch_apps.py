import os
from typing import Literal
from pathlib import Path

from modules import Logger
from modules.config import launch_apps


def start_launch_apps(mode: Literal["Player", "Studio"]) -> None:
    configured_apps: list[dict] = launch_apps.get_active(mode)

    if not configured_apps:
        Logger.info("No launch apps found!")
        return

    for item in configured_apps:
        try:
            filepath: str = item["filepath"]
        except KeyError:
            continue
        launch_args: str = item.get("launch_args", "")

        try:
            filepath_as_path: Path = Path(filepath)
            if not filepath_as_path.is_file():
                Logger.warning(f"File does not exist: {filepath_as_path.name}")
                continue
            
            os.startfile(filepath, arguments=launch_args)

        except Exception as e:
            Logger.warning(f"Failed to start launch app! {type(e).__name__}: {e}")