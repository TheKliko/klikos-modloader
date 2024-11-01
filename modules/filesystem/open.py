import os
import subprocess


def open(path: str) -> None:
    if os.path.isfile(path):
        path = os.path.dirname(path)
    
    if os.path.isdir(path):
        subprocess.Popen(f"explorer \"{path}\"")