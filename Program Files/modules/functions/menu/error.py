import os
import subprocess

from modules.filesystem import Directory


def show(name: str, text: str) -> None:
    filepath: str = os.path.join(Directory.program_files(), "modules", "exception_handler.py")
    new_command: str = "start cmd /c \"python \""+filepath+"\" \""+name+"\" \""+text+"\"\""
    subprocess.Popen(new_command, shell=True)