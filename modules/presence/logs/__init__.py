from typing import Literal, Optional

from . import reader


def read(mode: Literal["WindowsPlayer", "WindowsStudio"]) -> Optional[dict]:
    assert mode in ["WindowsPlayer", "WindowsStudio"]
    if mode == "WindowsPlayer":
        return reader.player()
    elif mode == "WindowsStudio":
        return reader.studio()