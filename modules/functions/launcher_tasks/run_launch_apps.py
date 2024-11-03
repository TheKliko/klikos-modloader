import os
from typing import Optional

from modules.logger import logger
from modules.filesystem import logged_path
from modules.functions.config import launch_integrations


def run_launch_apps() -> None:
    active_apps: list[tuple[str, Optional[str]]] = launch_integrations.get_active()
    if not active_apps:
        return
    
    for app, args in active_apps:
        try:
            if args:
                os.startfile(app, arguments=args)
            else:
                os.startfile(app)

        except Exception as e:
            logger.error(f"Failed to launch app {logged_path.get(app)}! {type(e).__name__}: {e}")