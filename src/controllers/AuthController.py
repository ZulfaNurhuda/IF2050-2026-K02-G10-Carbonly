from argon2 import PasswordHasher

from src.models.User import User
from src.services.AuthService import AuthService

_ph = PasswordHasher()


class AuthController:
    @staticmethod
    def login(username: str, password: str) -> tuple[bool, str]:
        if not username or not password:
            return False, "Please enter username and password"
        user = User.find_by_username(username)
        if user is None or user.password_hash is None:
            return False, "Invalid username or password"
        if not User.verify_password(user.password_hash, password):
            return False, "Invalid username or password"
        if user.id is not None and User.needs_rehash(user.password_hash):
            new_hash = _ph.hash(password)
            User.update_password(user.id, new_hash)
            user.password_hash = new_hash
        AuthService.set_current_user(user)
        AuthService.save_session()
        return True, ""

    @staticmethod
    def register(username: str, password: str, confirm: str) -> tuple[bool, str]:
        if not username or not password or not confirm:
            return False, "Please fill in all fields"
        if password != confirm:
            return False, "Passwords do not match"
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        if not User.create_user(username, password):
            return False, "Username already exists"
        return True, "Registration successful! Please login."

    @staticmethod
    def logout() -> None:
        AuthService.clear_session()

    @staticmethod
    def initialize() -> bool:
        user = AuthService.load_session()
        if user is None:
            return False
        AuthService.set_current_user(user)
        return True

    @staticmethod
    def get_current_username() -> str:
        user = AuthService.get_current_user()
        return (user.username or "") if user else ""

    @staticmethod
    def update_username(new_username: str) -> tuple[bool, str]:
        if not new_username:
            return False, "Username tidak boleh kosong"
        if len(new_username) < 3:
            return False, "Username minimal 3 karakter"
        user = AuthService.get_current_user()
        if user is None or user.id is None:
            return False, "Not logged in"
        if not User.update_username(user.id, new_username):
            return False, "Username sudah digunakan"
        user.username = new_username
        return True, "Username berhasil diperbarui"

    @staticmethod
    def update_password(current: str, new_pass: str, confirm: str) -> tuple[bool, str]:
        if not current or not new_pass or not confirm:
            return False, "Semua field harus diisi"
        if new_pass != confirm:
            return False, "Password baru tidak cocok"
        if len(new_pass) < 6:
            return False, "Password baru minimal 6 karakter"
        user = AuthService.get_current_user()
        if user is None or user.id is None or user.password_hash is None:
            return False, "Not logged in"
        if not User.verify_password(user.password_hash, current):
            return False, "Password saat ini salah"
        new_hash = _ph.hash(new_pass)
        User.update_password(user.id, new_hash)
        user.password_hash = new_hash
        return True, "Password berhasil diperbarui"
