import base64
import json
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.models.User import User

_APP_IDENTITY = b"carbonly-dekstop-app"
_KDF_SALT = b"carbonly-kdf-salt-v1"


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
    def get_current_user() -> Optional[User]:
        return AuthService._current_user

    @staticmethod
    def set_current_user(user: Optional[User]) -> None:
        AuthService._current_user = user

    @staticmethod
    def save_session() -> None:
        user = AuthService._current_user
        if user is None or user.id is None:
            return
        payload = json.dumps({"user_id": user.id}).encode()
        AuthService._SESSION_PATH.write_bytes(_get_fernet().encrypt(payload))

    @staticmethod
    def load_session() -> Optional[User]:
        if not AuthService._SESSION_PATH.exists():
            return None
        try:
            encrypted = AuthService._SESSION_PATH.read_bytes()
            payload = json.loads(_get_fernet().decrypt(encrypted))
            user = User.find_by_id(int(payload["user_id"]))
            if user is None:
                AuthService._SESSION_PATH.unlink(missing_ok=True)
            return user
        except (InvalidToken, Exception):
            AuthService._SESSION_PATH.unlink(missing_ok=True)
            return None

    @staticmethod
    def clear_session() -> None:
        AuthService._SESSION_PATH.unlink(missing_ok=True)
        AuthService._current_user = None
