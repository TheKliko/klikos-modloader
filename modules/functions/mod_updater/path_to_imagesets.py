import os


def get(root: str) -> str|None:
    for dirpath, dirnames, filenames in os.walk(root):
        for file in filenames:
            if file.startswith("img_set"):
                relative_path: str = os.path.dirname(os.path.join(os.path.relpath(os.path.join(dirpath, file), root)))
                return relative_path
    else:
        return None