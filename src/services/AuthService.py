import base64
import json
from pathlib import Path
from typing import Optional

from argon2 import PasswordHasher
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.models.User import User

_APP_IDENTITY = b"c4rb0nly-d3skt0p-2026"
_KDF_SALT = b"c4rb0nly-kdf-s4lt-v1"
_ph = PasswordHasher()


def _get_fernet() -> Fernet:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_KDF_SALT,
        iterations=100_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(_APP_IDENTITY))
    return Fernet(key)


class AuthService:
    _current_user: Optional[User] = None
    _SESSION_PATH: Path = (
        Path(__file__).resolve().parent.parent.parent / ".carbonly_session"
    )

    @staticmethod
    def verify_user(username: str, password: str) -> bool:
        user = User.find_by_username(username)
        if user is None or user.password_hash is None:
            return False
        if not User.verify_password(user.password_hash, password):
            return False
        if user.id is not None and User.needs_rehash(user.password_hash):
            new_hash = _ph.hash(password)
            User.update_password(user.id, new_hash)
            user.password_hash = new_hash
        AuthService._current_user = user
        return True

    @staticmethod
    def get_current_user() -> Optional[User]:
        return AuthService._current_user

    @staticmethod
    def save_session() -> None:
        user = AuthService._current_user
        if user is None or user.id is None:
            return
        payload = json.dumps({"user_id": user.id}).encode()
        AuthService._SESSION_PATH.write_bytes(_get_fernet().encrypt(payload))

    @staticmethod
    def load_session() -> bool:
        if not AuthService._SESSION_PATH.exists():
            return False
        try:
            encrypted = AuthService._SESSION_PATH.read_bytes()
            payload = json.loads(_get_fernet().decrypt(encrypted))
            user = User.find_by_id(int(payload["user_id"]))
            if user is None:
                AuthService._SESSION_PATH.unlink(missing_ok=True)
                return False
            AuthService._current_user = user
            return True
        except (InvalidToken, Exception):
            AuthService._SESSION_PATH.unlink(missing_ok=True)
            return False

    @staticmethod
    def clear_session() -> None:
        AuthService._SESSION_PATH.unlink(missing_ok=True)
        AuthService._current_user = None

    @staticmethod
    def get_user(username: str) -> User | None:
        return User.find_by_username(username)

    @staticmethod
    def register_user(username: str, password: str) -> tuple[bool, str]:
        if not username or not password:
            return False, "Username and password are required"
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        success = User.create_user(username, password)
        if not success:
            return False, "Username already exists"
        return True, "User registered successfully"

    @staticmethod
    def update_username(new_username: str) -> tuple[bool, str]:
        user = AuthService._current_user
        if user is None or user.id is None:
            return False, "Not logged in"
        if len(new_username) < 3:
            return False, "Username minimal 3 karakter"
        success = User.update_username(user.id, new_username)
        if not success:
            return False, "Username sudah digunakan"
        user.username = new_username
        return True, "Username berhasil diperbarui"

    @staticmethod
    def update_password(
        current_password: str, new_password: str
    ) -> tuple[bool, str]:
        user = AuthService._current_user
        if user is None or user.id is None or user.password_hash is None:
            return False, "Not logged in"
        if not User.verify_password(user.password_hash, current_password):
            return False, "Password saat ini salah"
        if len(new_password) < 6:
            return False, "Password baru minimal 6 karakter"
        new_hash = _ph.hash(new_password)
        User.update_password(user.id, new_hash)
        user.password_hash = new_hash
        return True, "Password berhasil diperbarui"
