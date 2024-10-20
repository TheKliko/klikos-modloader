import traceback

from modules.logger import logger


def run(e: Exception) -> None:
    logger.critical(f"Uncaught exception! {type(e).__name__}: {e}")
    logger.debug("".join(traceback.format_exception(type(e), e, e.__traceback__)))
    logger.info("If you need any help, please join our Discord server: https://discord.gg/nEjUwdSP9P")