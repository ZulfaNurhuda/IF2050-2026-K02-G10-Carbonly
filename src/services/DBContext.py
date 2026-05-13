import sqlite3
from collections.abc import Generator
from contextlib import contextmanager

from src.services.AppPaths import app_data_dir


class DBContext:
    _DB_PATH: str = str(app_data_dir() / "carbonly.db")

    @staticmethod
    @contextmanager
    def connect() -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(DBContext._DB_PATH)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
