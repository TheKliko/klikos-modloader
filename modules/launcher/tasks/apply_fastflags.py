from pathlib import Path
from typing import Literal
import json

from modules import Logger
from modules.config import fastflags, integrations


def apply_fastflags(version_folder_root: str | Path, mode: Literal["Player", "Studio"]) -> None:
    version_folder_root = Path(version_folder_root)
    
    Logger.info("Applying fastflags...")
    active_fastflags: dict = fastflags.get_active(mode)

    # Needed for RPC to work properly
    active_fastflags.update({
        "FLogNetwork": "7"
    })

    target: Path = version_folder_root / "ClientSettings" / "ClientAppSettings.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w") as file:
        json.dump(active_fastflags, file, indent=4)