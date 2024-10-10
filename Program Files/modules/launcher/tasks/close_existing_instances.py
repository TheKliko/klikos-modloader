import subprocess


def close_existing_instances(binary_type: str) -> None:
    subprocess.Popen(
        "taskkill /f /im Roblox"+str("Player" if "player" in binary_type.lower() else "Studio")+"Beta.exe",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )