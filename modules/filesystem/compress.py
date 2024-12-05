import os
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from modules import Logger

from .exceptions import FileCompressError


def compress(source: str | Path, destination: str | Path) -> None:
    source = Path(source)
    destination = Path(destination)

    Logger.info(f"Compressing file: {source.name}...")

    if destination.suffix != ".zip":
        raise FileCompressError(f"Target must be a .zip file: {destination.name}")

    if not os.access(destination.parent, os.W_OK):
        raise FileCompressError(f"Write permissions denied for {destination.parent}")

    os.makedirs(destination.parent, exist_ok=True)

    with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
        if source.is_file():
            archive.write(source, source.name)
        
        elif source.is_dir():
            for dirpath, dirnames, filenames in os.walk(source):
                dirpath = Path(dirpath)
                for filename in filenames:
                    filepath: Path = dirpath / filename
                    arcname: Path = filepath.relative_to(source)
                    archive.write(filepath, arcname)