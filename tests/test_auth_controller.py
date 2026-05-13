import pytest

from src.controllers.AuthController import AuthController
from src.services.AuthService import AuthService


@pytest.fixture(autouse=True)
def patch_session(monkeypatch):
    monkeypatch.setattr(AuthService, "save_session", lambda: None)
    monkeypatch.setattr(AuthService, "clear_session", lambda: None)
    yield
    AuthService.set_current_user(None)


class TestRegister:
    def test_success(self, db):
        ok, _ = AuthController.register("alice", "password123", "password123")
        assert ok is True

    def test_empty_fields(self, db):
        ok, _ = AuthController.register("", "password123", "password123")
        assert ok is False

    def test_password_mismatch(self, db):
        ok, _ = AuthController.register("alice", "password123", "different")
        assert ok is False

    def test_username_too_short(self, db):
        ok, msg = AuthController.register("ab", "password123", "password123")
        assert ok is False
        assert "3" in msg

    def test_password_too_short(self, db):
        ok, msg = AuthController.register("alice", "abc", "abc")
        assert ok is False
        assert "6" in msg

    def test_duplicate_username(self, db):
        AuthController.register("alice", "password123", "password123")
        ok, _ = AuthController.register("alice", "password456", "password456")
        assert ok is False


class TestLogin:
    def test_success(self, db):
        AuthController.register("alice", "password123", "password123")
        ok, _ = AuthController.login("alice", "password123")
        assert ok is True
        assert AuthService.get_current_user() is not None

    def test_wrong_password(self, db):
        AuthController.register("alice", "password123", "password123")
        ok, _ = AuthController.login("alice", "wrongpass")
        assert ok is False

    def test_nonexistent_user(self, db):
        ok, _ = AuthController.login("nobody", "password123")
        assert ok is False

    def test_empty_fields(self, db):
        ok, _ = AuthController.login("", "")
        assert ok is False


class TestUpdateUsername:
    def test_success(self, db):
        AuthController.register("alice", "password123", "password123")
        AuthController.login("alice", "password123")
        ok, _ = AuthController.update_username("alice_new")
        assert ok is True

    def test_same_username(self, db):
        AuthController.register("alice", "password123", "password123")
        AuthController.login("alice", "password123")
        ok, _ = AuthController.update_username("alice")
        assert ok is False

    def test_too_short(self, db):
        AuthController.register("alice", "password123", "password123")
        AuthController.login("alice", "password123")
        ok, _ = AuthController.update_username("ab")
        assert ok is False


class TestUpdatePassword:
    def test_success(self, db):
        AuthController.register("alice", "password123", "password123")
        AuthController.login("alice", "password123")
        ok, _ = AuthController.update_password("password123", "newpass123", "newpass123")
        assert ok is True

    def test_wrong_current_password(self, db):
        AuthController.register("alice", "password123", "password123")
        AuthController.login("alice", "password123")
        ok, _ = AuthController.update_password("wrongpass", "newpass123", "newpass123")
        assert ok is False

    def test_same_as_current(self, db):
        AuthController.register("alice", "password123", "password123")
        AuthController.login("alice", "password123")
        ok, _ = AuthController.update_password("password123", "password123", "password123")
        assert ok is False

    def test_confirm_mismatch(self, db):
        AuthController.register("alice", "password123", "password123")
        AuthController.login("alice", "password123")
        ok, _ = AuthController.update_password("password123", "newpass123", "different")
        assert ok is False

    def test_new_too_short(self, db):
        AuthController.register("alice", "password123", "password123")
        AuthController.login("alice", "password123")
        ok, _ = AuthController.update_password("password123", "abc", "abc")
        assert ok is False
