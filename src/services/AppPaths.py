import sys
from pathlib import Path

from platformdirs import user_data_dir

_APP_NAME = "Carbonly"
_APP_AUTHOR = "Carbonly"


def app_data_dir() -> Path:
    path = Path(user_data_dir(_APP_NAME, _APP_AUTHOR, roaming=True))
    path.mkdir(parents=True, exist_ok=True)
    return path


def resource_path(relative: str) -> str:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent.parent))
    return str(base / relative)
