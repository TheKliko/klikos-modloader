import importlib.util


REQUIRED_LIBRARIES: list[str] = [
    "requests",
    "pypresence",
    "PIL",
    "customtkinter",
    "py7zr"
]


def check_required_libraries() -> None:
    missing_libraries: list[str] = []
    for library in REQUIRED_LIBRARIES:
        if not is_installed(library):
            missing_libraries.append(library)
    
    if missing_libraries == []:
        return
    
    raise Exception(f"The following libraries are missing: {', '.join(missing_libraries)}")


def is_installed(library: str) -> bool:
    return importlib.util.find_spec(library) is not None