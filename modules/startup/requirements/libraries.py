import importlib.util
from pathlib import Path
import sys
import os


REQUIRED_LIBRARIES: list[str] = [
    "requests",
    "pypresence",
    "pyperclip",
    "customtkinter",
    "PIL",
    "psutil",
    "fontTools",
    "numpy"
]


def check_required_libraries() -> None:
    missing_libraries: list[str] = []
    for library in REQUIRED_LIBRARIES:
        if not is_installed(library):
            missing_libraries.append(library)
    
    if missing_libraries != []:
        raise Exception(f"The following libraries are missing: {', '.join(missing_libraries)}")

    libraries_path: Path = Path(__file__).parent / "libraries"
    os.makedirs(libraries_path.parent, exist_ok=True)
    sys.path.insert(0, str(libraries_path))


def is_installed(library: str) -> bool:
    return importlib.util.find_spec(library) is not None