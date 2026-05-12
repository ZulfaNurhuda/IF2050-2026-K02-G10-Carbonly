import sqlite3
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import (
    HashingError,
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)

from src.services.DBContext import DBContext

_ph = PasswordHasher()


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
        demo_username = "CarbonlyAdmin"
        demo_password = "123456"  # nosec B105
        try:
            with DBContext.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id FROM users WHERE username = ?", (demo_username,)
                )
                if cursor.fetchone() is None:
                    password_hash = _ph.hash(demo_password)
                    cursor.execute(
                        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                        (demo_username, password_hash),
                    )
        except (sqlite3.Error, HashingError):
            pass

    @staticmethod
    def find_by_username(username: str) -> Optional["User"]:
        try:
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
        except sqlite3.Error:
            return None

    @staticmethod
    def create_user(username: str, password: str) -> bool:
        try:
            with DBContext.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                if cursor.fetchone() is not None:
                    return False
                password_hash = _ph.hash(password)
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash),
                )
            return True
        except (sqlite3.Error, HashingError):
            return False

    @staticmethod
    def find_by_id(user_id: int) -> Optional["User"]:
        try:
            with DBContext.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, username, password_hash FROM users WHERE id = ?",
                    (user_id,),
                )
                row = cursor.fetchone()
            if row:
                return User(id=row[0], username=row[1], password_hash=row[2])
            return None
        except sqlite3.Error:
            return None

    @staticmethod
    def update_username(user_id: int, new_username: str) -> bool:
        try:
            with DBContext.connect() as conn:
                conn.execute(
                    "UPDATE users SET username = ? WHERE id = ?",
                    (new_username, user_id),
                )
            return True
        except sqlite3.Error:
            return False

    @staticmethod
    def update_password(user_id: int, new_password_hash: str) -> bool:
        try:
            with DBContext.connect() as conn:
                conn.execute(
                    "UPDATE users SET password_hash = ? WHERE id = ?",
                    (new_password_hash, user_id),
                )
            return True
        except sqlite3.Error:
            return False

    @staticmethod
    def verify_password(stored_hash: str, password: str) -> bool:
        try:
            _ph.verify(stored_hash, password)
            return True
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            return False

    @staticmethod
    def needs_rehash(stored_hash: str) -> bool:
        return bool(_ph.check_needs_rehash(stored_hash))
