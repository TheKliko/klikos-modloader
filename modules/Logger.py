import logging
from pathlib import Path
from datetime import datetime, timedelta
import sys
import inspect
import platform

from modules import LaunchMode
from modules.info import ProjectData


IS_FROZEN: bool = getattr(sys, "frozen", False)
if IS_FROZEN:
    ROOT: Path = Path(sys.executable).parent
else:
    ROOT = Path(__file__).parent.parent


TIMESTAMP: str = datetime.now().strftime("%Y-%m-%d@%H-%M-%S.%f")
LAUNCH_MODE: str = LaunchMode.get()
FILENAME: str = f"{TIMESTAMP}_{LAUNCH_MODE.upper()}.log"
LOG_DIRECTORY: Path = Path(ROOT, "Logs")
FILEPATH: Path = Path(LOG_DIRECTORY, FILENAME)

MAX_LOG_AGE: int = 7  # DAYS


def initialize() -> None:
    FILEPATH.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=FILEPATH,
        level=logging.DEBUG,
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d@%H:%M:%S",
        encoding="utf-8"
    )
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("pyi_splash").setLevel(logging.WARNING)

    debug(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    debug(f"Platform: {platform.system()} {platform.release()}")
    debug(f"System Architecture: {platform.architecture()[0]}")
    debug(f"Project version: {ProjectData.VERSION}")
    debug(f"Launch mode: {LAUNCH_MODE}")

    launch_arguments: list | None = sys.argv[1:]
    if not launch_arguments:
        launch_arguments = None
    debug(f"Launch arguments: {launch_arguments}")

    remove_old_logs()


def remove_old_logs() -> None:
    for log in LOG_DIRECTORY.iterdir():
        if not log.is_file():
            continue

        age: timedelta = datetime.now() - datetime.fromtimestamp(log.stat().st_mtime)
        if age > timedelta(days=MAX_LOG_AGE):
            try:
                log.unlink()
                debug(f"Removed old log: {log.name}")
            except Exception as e:
                warning(f"Failed to remove old log: {log.name}! {type(e).__name__}: {e}")


def get_prefix() -> str:
        UNKNOWN: str = "unknown()"
        frame = inspect.currentframe()
        if frame is None:
            return UNKNOWN
        frame = frame.f_back
        if frame is None:
            return UNKNOWN
        frame = frame.f_back
        if frame is None:
            return UNKNOWN

        filepath: Path = Path(frame.f_code.co_filename)
        module: str = filepath.parent.stem if filepath.stem == "__init__" else filepath.stem
        function: str = frame.f_code.co_name
        return f"{module}.{function}()"


def info(message: object) -> None:
    logging.info(f"[{get_prefix()}] {message}")


def warning(message: object) -> None:
    logging.warning(f"[{get_prefix()}] {message}")


def error(message: object, exc_info = None) -> None:
    logging.error(f"[{get_prefix()}] {message}", exc_info=exc_info)


def debug(message: object) -> None:
    logging.debug(f"[{get_prefix()}] {message}")


def critical(message: object, exc_info = None) -> None:
    logging.critical(f"[{get_prefix()}] {message}", exc_info=exc_info)


initialize()