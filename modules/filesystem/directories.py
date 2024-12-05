from pathlib import Path


class Directory:
    ROOT: Path = Path(__file__).parent.parent.parent
    INSTALLER: Path = ROOT / "Installer"
    UNINSTALLER: Path = ROOT / "Uninstaller"
    DOWNLOADS: Path = ROOT / "Downloads"
    CONFIG: Path = ROOT / "config"
    VERSIONS: Path = ROOT / "Versions"
    MODS: Path = ROOT / "Mods"