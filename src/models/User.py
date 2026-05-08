import hashlib
import sqlite3
from pathlib import Path
from typing import Optional


class User:
    _DB_PATH = str(Path(__file__).resolve().parent.parent.parent / "carbonly.db")

    def __init__(
        self,
        id: Optional[int] = None,
        username: Optional[str] = None,
        password_hash: Optional[str] = None,
    ):
        self._id = id
        self._username = username
        self._password_hash = password_hash

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]):
        self._id = value

    @property
    def username(self) -> Optional[str]:
        return self._username

    @username.setter
    def username(self, value: Optional[str]):
        self._username = value

    @property
    def password_hash(self) -> Optional[str]:
        return self._password_hash

    @password_hash.setter
    def password_hash(self, value: Optional[str]):
        self._password_hash = value

    @staticmethod
    def _get_connection() -> sqlite3.Connection:
        return sqlite3.connect(User._DB_PATH)

    @staticmethod
    def create_table() -> None:
        conn = User._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def seed_demo_user() -> None:
        conn = User._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
        if cursor.fetchone() is None:
            password_hash = hashlib.sha256("123456".encode()).hexdigest()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                ("admin", password_hash),
            )
            conn.commit()
        conn.close()

    @staticmethod
    def find_by_username(username: str) -> Optional["User"]:
        conn = User._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(id=row[0], username=row[1], password_hash=row[2])
        return None

    @staticmethod
    def create_user(username: str, password: str) -> bool:
        conn = User._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone() is not None:
                conn.close()
                return False
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False