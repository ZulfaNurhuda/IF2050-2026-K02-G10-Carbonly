import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path


class DBContext:
    _DB_PATH: str = str(Path(__file__).resolve().parent.parent.parent / "carbonly.db")

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
