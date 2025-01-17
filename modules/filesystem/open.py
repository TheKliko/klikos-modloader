from pathlib import Path
import subprocess

from modules import Logger


def open(path: str | Path) -> None:
    path = Path(path)

    if path.is_file():
        path = path.parent
    
    Logger.info("Opening file explorer...", prefix="filesystem.open()")
    subprocess.Popen(f"explorer \"{path}\"")