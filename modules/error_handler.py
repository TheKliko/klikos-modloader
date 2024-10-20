import traceback

from modules.logger import logger
from modules.info import Hyperlink


def run(e: Exception) -> None:
    logger.critical(f"Uncaught exception! {type(e).__name__}: {e}")
    logger.debug("".join(traceback.format_exception(type(e), e, e.__traceback__)))
    logger.info(f"If you need any help, please join our Discord server: {Hyperlink.DISCORD}")