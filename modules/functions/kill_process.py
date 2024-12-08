import subprocess


def kill_process(process: str) -> None:
    command: str = f"TASKKILL /F /IM {process}"
    subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)