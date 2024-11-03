from typing import Optional

from modules.filesystem import Directory
from modules.functions.config import integrations


ROBLOX_LOGS_DIRECTORY: str = Directory.roblox_logs()


# region Player
def player() -> Optional[dict]:
    activity_joining: Optional[bool] = integrations.value("activity_joining")
    return None



# region Studio
def studio() -> Optional[dict]:
    pass