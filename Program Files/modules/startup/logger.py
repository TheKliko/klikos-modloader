import glob
import logging
import os
import time

from modules.filesystem.directories import Directory


def start(filename: str|None = None) -> None:
    logging_directory: str = Directory.logs()
    log_filename: str = "log_"+str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))+".log"
    if filename:
        log_filename = "log_"+str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))+"_"+filename+".log"
    log_filepath: str = os.path.join(logging_directory, log_filename)

    os.makedirs(logging_directory, exist_ok=True)

    logging.basicConfig(
        filename=log_filepath,
        level=logging.DEBUG,
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(module)s.%(funcName)s()@line_%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d_%H:%M:%S",
        encoding="utf-8"
    )
    logging.getLogger("PIL").setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.info("Writing logs to: "+log_filename)


def clear_old_logs() -> None:
    logging_directory: str = Directory.logs()

    logs: list = sorted(
        (entry for entry in os.scandir(logging_directory) if entry.is_file() and entry.name.endswith(".log")),
        key=lambda entry: entry.stat().st_birthtime
    )[:-10]

    if not logs:
        logging.info("No logs removed.")
        return

    counter: int = 0
    for log in logs:
        try:
            os.remove(log.path)
            counter += 1
        except Exception as e:
            logging.warning("Failed to remove log file: "+log.name)
            logging.warning(type(e).__name__+": "+str(e))
    logging.info("Removed "+str(counter)+" log files.")