import psutil
from psutil import NoSuchProcess


class ProcessCheckError(Exception):
    pass


def process_exists(process: str) -> bool:
    for p in psutil.process_iter():
        try:
            if p.name() == process:
                return True

        except NoSuchProcess:
            continue

    return False