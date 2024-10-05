import os

from modules import variables


def title(title: str = None) -> None:
    os.system("title "+(title or "Python "+variables.get("python_version")))