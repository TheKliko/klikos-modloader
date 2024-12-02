import psutil
from psutil import NoSuchProcess


class ProcessCheckError(Exception):
    pass


def process_exists(process: str) -> bool:
    for _ in range(5):
        try:
            return any(p.name() == process for p in psutil.process_iter())

        except NoSuchProcess:
            continue
    
    raise ProcessCheckError(f"Ran out of attempts when checking for \"{process}\"")