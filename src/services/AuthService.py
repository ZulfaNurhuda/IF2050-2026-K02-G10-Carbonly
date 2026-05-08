import hashlib
import hmac
import json
from pathlib import Path
from typing import Optional

from src.models.User import User

_SESSION_SIGN_KEY = b"c4rb0nly-d3skt0p-2026"


class AuthService:
    _current_user: Optional[User] = None
    _SESSION_PATH: Path = (
        Path(__file__).resolve().parent.parent.parent / ".carbonly_session"
    )

    @staticmethod
    def _sign(user_id: int) -> str:
        return hmac.digest(
            _SESSION_SIGN_KEY, str(user_id).encode(), hashlib.sha256
        ).hex()

    @staticmethod
    def verify_user(username: str, password: str) -> bool:
        user = User.find_by_username(username)
        if user is None:
            return False
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash == password_hash:
            AuthService._current_user = user
            return True
        return False

    @staticmethod
    def get_current_user() -> Optional[User]:
        return AuthService._current_user

    @staticmethod
    def save_session() -> None:
        user = AuthService._current_user
        if user is None or user.id is None:
            return
        payload = {"user_id": user.id, "sig": AuthService._sign(user.id)}
        AuthService._SESSION_PATH.write_text(json.dumps(payload))

    @staticmethod
    def load_session() -> bool:
        if not AuthService._SESSION_PATH.exists():
            return False
        try:
            data = json.loads(AuthService._SESSION_PATH.read_text())
            user_id = int(data["user_id"])
            if not hmac.compare_digest(str(data["sig"]), AuthService._sign(user_id)):
                AuthService._SESSION_PATH.unlink(missing_ok=True)
                return False
            user = User.find_by_id(user_id)
            if user is None:
                AuthService._SESSION_PATH.unlink(missing_ok=True)
                return False
            AuthService._current_user = user
            return True
        except Exception:
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
        if user is None or user.id is None:
            return False, "Not logged in"
        current_hash = hashlib.sha256(current_password.encode()).hexdigest()
        if user.password_hash != current_hash:
            return False, "Password saat ini salah"
        if len(new_password) < 6:
            return False, "Password baru minimal 6 karakter"
        new_hash = hashlib.sha256(new_password.encode()).hexdigest()
        User.update_password(user.id, new_hash)
        user.password_hash = new_hash
        return True, "Password berhasil diperbarui"
