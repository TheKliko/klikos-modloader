import os


def get(root: str) -> str:
    for dirpath, dirnames, filenames in os.walk(root):
        if "GetImageSetData.lua" in filenames:
            relative_path: str = os.path.join(os.path.relpath(os.path.join(dirpath, "GetImageSetData.lua"), root))
            return relative_path
    else:
        return None