from . import logger
from . import settings
from . import update
from .check_required_files import check_required_files
from .clear_old_logs import clear_old_logs

from modules.interface import Print, Color
from modules.other.paths import Directory, FilePath
from modules.utils.registry_editor import set_registry_keys


def run() -> None:
    Directory.initialize()
    FilePath.initialize()

    logger.start()
    check_required_files()
    settings.load()
    clear_old_logs()

    Print('Setting registry keys . . .', color=Color.INITALIZE)
    set_registry_keys()

    update.check_for_updates()