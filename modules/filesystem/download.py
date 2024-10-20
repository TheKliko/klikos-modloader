import os
import urllib
import urllib.request
import time

from modules.logger import logger


COOLDOWN: int = 2


def download(url: str, destination: str, attempts: int = 3) -> None:
    logger.info(f"Attempting file download: {url}")
    try:
        os.makedirs(destination, exist_ok=True)
        urllib.request.urlretrieve(url, destination)
        logger.info(f"File downloaded successfully: {url}")
    
    except Exception as e:
        logger.warning(f"File download failed: {url}, reason: {type(e).__name__}! {e}")

        if attempts <= 0:
            logger.error(f"File download failed: {url}, reason: Too many attemps!")
            raise

        time.sleep(COOLDOWN)
        logger.info("Retrying . . .")
        return download(url=url, destination=destination, attempts=attempts-1)
        
