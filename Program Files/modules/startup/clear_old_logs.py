import glob
import logging
import os

from modules.interface import Print, Color
from modules.utils import variables
from modules.other.paths import Directory


def clear_old_logs() -> None:
    logging.info('Checking for old logs . . .')

    log_directory: str = Directory.LOGS
    logs: list = sorted(glob.glob(os.path.join(log_directory, "*.log")), key=os.path.getctime, reverse=True)

    data: dict = variables.get('max_log_files', {})
    max_log_files: int = data.get('value', data.get('default', 10))

    if len(logs) <= max_log_files:
        return
    
    old_logs: list[str] = logs[max_log_files:]
    for log in old_logs:
        logging.info('Clearing old logs . . .')
        Print('Clearing old logs . . .', color=Color.INITALIZE)
        try:
            os.remove(log)
            logging.info(f'Removed old log: {os.path.basename(log)}')
        
        except PermissionError as e:
            logging.warning(f'[{type(e).__name__}] Failed to remove log: {os.path.basename(log)}')
        
        except FileNotFoundError as e:
            continue