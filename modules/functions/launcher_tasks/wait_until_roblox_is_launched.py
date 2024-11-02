import time

from modules.logger import logger
from modules.functions.process_exists import process_exists


COOLDOWN: float = 0.1


def wait_until_roblox_is_launched(executable: str) -> None:
    logger.info("Waiting until Roblox is launched...")
    while not process_exists(executable):
        time.sleep(COOLDOWN)
    logger.info("Roblox launch confirmed!")