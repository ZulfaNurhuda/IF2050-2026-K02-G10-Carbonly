import hashlib
import sqlite3
from typing import Optional

from src.services.DBContext import DBContext


class User:
    def __init__(
        self,
        id: Optional[int] = None,
        username: Optional[str] = None,
        password_hash: Optional[str] = None,
    ) -> None:
        self._id = id
        self._username = username
        self._password_hash = password_hash

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        self._id = value

    @property
    def username(self) -> Optional[str]:
        return self._username

    @username.setter
    def username(self, value: Optional[str]) -> None:
        self._username = value

    @property
    def password_hash(self) -> Optional[str]:
        return self._password_hash

    @password_hash.setter
    def password_hash(self, value: Optional[str]) -> None:
        self._password_hash = value

    @staticmethod
    def create_table() -> None:
        with DBContext.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            """)

    @staticmethod
    def seed_demo_user() -> None:
        with DBContext.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
            if cursor.fetchone() is None:
                password_hash = hashlib.sha256("123456".encode()).hexdigest()
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    ("admin", password_hash),
                )

    @staticmethod
    def find_by_username(username: str) -> Optional["User"]:
        with DBContext.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, password_hash FROM users WHERE username = ?",
                (username,),
            )
            row = cursor.fetchone()
        if row:
            return User(id=row[0], username=row[1], password_hash=row[2])
        return None

    @staticmethod
    def create_user(username: str, password: str) -> bool:
        try:
            with DBContext.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                if cursor.fetchone() is not None:
                    return False
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash),
                )
            return True
        except sqlite3.IntegrityError:
            return False
