import sys
from pathlib import Path

from modules.filesystem import File, restore_from_meipass


IS_FROZEN: bool = getattr(sys, "frozen", False)


def check_required_files() -> None:
    missing_files: list[Path] = []

    for file in File.REQUIRES_FILES:
        file_exists: bool = file.is_file()

        if file_exists and not IS_FROZEN:
            continue

        elif not file_exists and not IS_FROZEN:
            missing_files.append(file)

        elif not file_exists and IS_FROZEN:
            restore_from_meipass(file)

        elif file_exists and IS_FROZEN:
            pass


        # match file.is_file(), IS_FROZEN:
        #     case True, True:
        #         pass

        #     case True, False:
        #         pass

        #     case False, True:
        #         pass

        #     case False, False:
        #         pass


        # file_exists: bool = file.is_file()
        # if file_exists and IS_FROZEN:
        #     pass
        # elif file_exists and not IS_FROZEN:
        #     pass
        # else:
        #     pass