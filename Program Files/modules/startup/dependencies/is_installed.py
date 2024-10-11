import importlib.util


def is_installed(library: str) -> bool:
    spec = importlib.util.find_spec(library)
    return spec is not None