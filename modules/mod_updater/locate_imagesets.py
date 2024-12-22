from pathlib import Path
import os

from .exceptions import ImageSetsNotFoundError


FILENAME: str = "img_set_1x_1.png"


def locate_imagesets(start: Path) -> Path:
    for dirpath, dirnames, filenames in os.walk(start):
        if FILENAME not in filenames:
            continue
        return Path(dirpath).relative_to(start)
    raise ImageSetsNotFoundError(f"Failed to find path to ImageSets")