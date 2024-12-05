from pathlib import Path

from .directories import Directory


class File:
    SETTINGS: Path = Directory.CONFIG / "settings.json"
    INTEGRATIONS: Path = Directory.CONFIG / "integrations.json"
    LAUNCH_INTEGRATIONS: Path = Directory.CONFIG / "launch_integrations.json"

    REQUIRES_FILES: list[Path] = [
        SETTINGS,
        INTEGRATIONS
    ]