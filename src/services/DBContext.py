import sqlite3
from pathlib import Path


class DBContext:
    _DB_PATH: str = str(Path(__file__).resolve().parent.parent.parent / "carbonly.db")

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        return sqlite3.connect(DBContext._DB_PATH)
