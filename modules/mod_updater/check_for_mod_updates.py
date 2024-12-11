from typing import Literal
from pathlib import Path
import json

from modules import Logger

from .deploy_history import DeployHistory, get_deploy_history
from .locate_imagesets import locate_imagesets
from .exceptions import ImageSetsNotFoundError


def check_for_mod_updates(directory: str | Path, mods: list[str], version: str) -> dict[str, list[Path]] | Literal[False]:
    Logger.info("Checking for mod updates...")
    directory = Path(directory)

    deploy_history: DeployHistory = get_deploy_history(version)
    version_hash: str = deploy_history.get_hash(version)

    result: dict[str, list[Path]] = {}
    for mod in mods:
        filepath: Path = directory / mod / "info.json"
        if not filepath.is_file():
            continue

        try:
            with open(filepath, "r") as file:
                data: dict = json.load(file)

            if "clientVersionUpload" not in data:
                continue

            mod_version: str = data["clientVersionUpload"]
            mod_hash: str = deploy_history.get_hash(mod_version)

            if version_hash == mod_hash:
                continue

            # Confirm that the mod actually changes the ImageSets
            try:
                locate_imagesets(directory / mod)
            except ImageSetsNotFoundError:
                continue

            if mod_hash not in result:
                result[mod_hash] = []
                result[mod_hash].append(directory / mod)

        except Exception as e:
            Logger.error(f"Failed to check updates for mod: {mod}. {type(e).__name__}: {e}")
            continue

    if not result:
        Logger.info("No mod updates found!")
        return False
    
    return result