from pathlib import Path

from .directories import Directory


class File:
    SETTINGS: Path = Directory.CONFIG / "settings.json"
    SPECIAL_SETTINGS: Path = Directory.CONFIG / "special_settings.json"
    INTEGRATIONS: Path = Directory.CONFIG / "integrations.json"
    MODS: Path = Directory.CONFIG / "mods.json"
    FASTFLAGS: Path = Directory.CONFIG / "fastflags.json"
    LAUNCH_INTEGRATIONS: Path = Directory.CONFIG / "launch_integrations.json"

    GLOBAL_BASIC_SETTINGS: Path = Directory.ROBLOX / "GlobalBasicSettings_13.xml"

    REQUIRED_FILES: list[Path] = [
        SETTINGS,
        INTEGRATIONS
    ]