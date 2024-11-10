import os
import urllib
import urllib.request
import time

from modules.logger import logger


COOLDOWN: int = 2


def download(url: str, destination: str, attempts: int = 3) -> None:
    try:
        logger.info(f"Attempting file download: {url}")
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        urllib.request.urlretrieve(url, destination)
        logger.info(f"File downloaded successfully: {url}")
    
    except Exception as e:
        logger.warning(f"File download failed: {url}, reason: {type(e).__name__}! {e}")

        if attempts <= 0:
            logger.error(f"File download failed: {url}, reason: Too many attempts!")
            raise

        logger.warning(f"Remaining attempts: {attempts}")
        logger.info(f"Retrying in {COOLDOWN} seconds...")
        time.sleep(COOLDOWN)
        return download(url=url, destination=destination, attempts=attempts-1)
        
