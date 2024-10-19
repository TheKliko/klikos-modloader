from modules.logger import logger
from modules import startup
from modules import launch_mode

import pyi_splash


def main():
    startup.run()
    pyi_splash.close()

    mode: str = launch_mode.get()
    logger.info(f"Launch mode: {mode}")


if __name__ == "__main__":
    main()