import os
import json

from modules.logger import logger
from modules.filesystem import Directory
from modules.functions.config import fastflags


def apply_fastflags(version: str) -> None:
    logger.info("Applying FastFlags...")
    target: str = os.path.join(Directory.versions(), version, "ClientSettings", "ClientAppSettings.json")
    if os.path.isfile(target):
        os.remove(target)
    os.makedirs(os.path.dirname(target), exist_ok=True)

    data: dict = fastflags.get_active()

    # Force FLogNetwork: 7
    data.update({
        "FLogNetwork": "7"
    })
    
    with open(target, "w") as file:
        json.dump(data, file, indent=4)