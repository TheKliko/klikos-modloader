from pathlib import Path
import os

from .exceptions import ImageSetDataNotFoundError


FILENAME: str = "GetImageSetData.lua"


def locate_imagesetdata_file(start: Path) -> Path:
    for dirpath, dirnames, filenames in os.walk(start):
        if FILENAME not in filenames:
            continue
        return Path(dirpath, FILENAME).relative_to(start)
    raise ImageSetDataNotFoundError(f"File not found: {FILENAME}")