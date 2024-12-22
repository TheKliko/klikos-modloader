import sys
from pathlib import Path

from .requirements.libraries import check_required_libraries
from .check_for_updates import check_for_updates


def run() -> None:
    # Only check for libraries if the program is running as a Python file instead of an executable
    if not getattr(sys, "frozen", False):
        check_required_libraries()

    from .requirements.files import check_required_files
    check_required_files()

    check_for_updates()