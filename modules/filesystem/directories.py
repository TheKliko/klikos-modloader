from pathlib import Path
import sys


class Directory:
    ROOT: Path = Path(__file__).parent.parent.parent if not getattr(sys, "frozen", False) else Path(sys.executable).parent
    INSTALLER: Path = ROOT / "Installer"
    UNINSTALLER: Path = ROOT / "Uninstaller"
    DOWNLOADS: Path = ROOT / "Downloads"
    CONFIG: Path = ROOT / "config"
    RESOURCES: Path = ROOT / "resources"
    THEMES: Path = RESOURCES / "themes"
    VERSIONS: Path = ROOT / "Versions"
    MODS: Path = ROOT / "Mods"

    LOCALAPPDATA: Path = Path.home() / "AppData" / "Local"
    ROBLOX: Path = LOCALAPPDATA / "Roblox"
    ROBLOX_LOGS: Path = ROBLOX / "logs"