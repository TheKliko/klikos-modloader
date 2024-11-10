import os
import shutil

from modules.logger import logger
from modules.filesystem import Directory


def apply_mods(mods: list[str], version: str) -> None:
    logger.info("Applying mods...")
    for mod in mods:
        try:
            shutil.copytree(mod, os.path.join(Directory.versions(), version), dirs_exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to apply mod \"{os.path.basename(mod)}\", reason: {type(e).__name__}: {e}")