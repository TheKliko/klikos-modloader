from pathlib import Path
import json

from modules import Logger
from modules.config import fastflags


def apply_fastflags(version_folder_root: str | Path) -> None:
    version_folder_root = Path(version_folder_root)
    
    Logger.info("Applying fastflags...")
    active_fastflags: dict = fastflags.get_active()

    # Needed for RPC to work properly
    active_fastflags.update({
        "FLogNetwork": "7"
    })

    target: Path = version_folder_root / "ClientSettings" / "ClientAppSettings.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w") as file:
        json.dump(active_fastflags, file, indent=4)