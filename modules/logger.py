import logging
import time
import os
import sys
import platform
from typing import Optional
import inspect
import threading

from modules.info import ProjectData


IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    root = os.path.dirname(sys.executable)
else:
    root = os.path.dirname(os.path.dirname(__file__))


class Logger:
    directory: str = os.path.join(root, "Logs")
    filename: str
    filepath: str
    MAX_LOG_COUNT: int = 20


    def __init__(self, name: Optional[str] = None) -> None:
        os.makedirs(self.directory, exist_ok=True)

        timestamp: str = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        if name:
            self.filename = f"{timestamp}_{name}.log"
        else:
            self.filename = f"{timestamp}.log"
        self.filepath = os.path.join(self.directory, self.filename)

        logging.basicConfig(
            filename=self.filepath,
            level=logging.DEBUG,
            format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d@%H:%M:%S",
            encoding="utf-8"
        )
        logging.getLogger("PIL").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("pyi_splash").setLevel(logging.WARNING)

        self.info(f"Writing logs to: {self.filename}")

        self._log_debug_info()
        self._remove_old_logs()
        threading.Thread(
            name="logger._remove_old_logs()_thread",
            target=self._remove_old_logs,
            daemon=True
        ).start()


    def _log_debug_info(self) -> None:
        self.debug(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        self.debug(f"Platform: {platform.system()} {platform.release()}")
        self.debug(f"System Architecture: {platform.architecture()[0]}")
        self.debug(f"Project version: {ProjectData.VERSION}")

        launch_arguments: list | None = sys.argv[1:]
        if not launch_arguments:
            launch_arguments = None
        self.debug(f"Launch arguments: {launch_arguments}")


    def _remove_old_logs(self) -> None:
        logs: list = [os.path.join(self.directory, log) for log in os.listdir(self.directory)]
        log_count: int = len(logs)

        if log_count <= self.MAX_LOG_COUNT:
            return

        old_log_count: int = log_count - self.MAX_LOG_COUNT
        self.info(f"Removing {old_log_count} log file{'s' if old_log_count > 1 else ''}...")

        for log in sorted(logs, key=os.path.getctime)[:old_log_count]:
            try:
                if os.path.isfile(log):
                    os.remove(log)
                    self.info(f"Removed old log file: {os.path.basename(log)}")
            except (PermissionError, OSError) as e:
                self.warning(f"Failed to remove log file: {os.path.basename(log)}, reason: {type(e).__name__}")
            except Exception as e:
                self.error(f"Failed to remove log file: {os.path.basename(log)}, reason: {type(e).__name__}! {e}")
    

    def _get_log_prefix(self) -> str:
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

        filename = os.path.basename(frame.f_code.co_filename).removesuffix(".py")
        function_name = frame.f_code.co_name
        return f"{filename}.{function_name}()"


    def info(self, message: object) -> None:
        logging.info(f"[{self._get_log_prefix()}] {message}")


    def warning(self, message: object) -> None:
        logging.warning(f"[{self._get_log_prefix()}] {message}")
    

    def error(self, message: object) -> None:
        logging.error(f"[{self._get_log_prefix()}] {message}")
    

    def debug(self, message: object) -> None:
        logging.debug(f"[{self._get_log_prefix()}] {message}")
    

    def critical(self, message: object) -> None:
        logging.critical(f"[{self._get_log_prefix()}] {message}")


logger = Logger()