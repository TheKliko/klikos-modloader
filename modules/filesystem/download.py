from pathlib import Path
import urllib.request
import os
import time

from modules import Logger

from .exceptions import FileDownloadError


COOLDOWN: float = 2


def download(source: str, destination: str | Path, attempts: int = 3) -> None:
    destination = Path(destination)
    temp: Path = destination.with_suffix(".tmp")
    exception: Exception | None = None

    for _ in range(attempts):
        try:
            Logger.info(f"Downloading file: {source}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            if not os.access(destination.parent, os.W_OK):
                raise FileDownloadError(f"Write permissions denied for {destination.parent}")

            try:
                urllib.request.urlretrieve(source, temp)
                os.replace(temp, destination)
                return
            except Exception as e:
                if temp.is_file():
                    temp.unlink()
                raise

        except Exception as e:
            Logger.error(f"File download failed! {type(e).__name__}: {e}")
            exception = e
            time.sleep(COOLDOWN)
    
    if exception is not None:
        raise exception