from argon2 import PasswordHasher

from src.models.User import User

_ph = PasswordHasher()


class TestCreateAndFind:
    def test_create_success(self, db):
        assert User.create_user("alice", "password123") is True

    def test_create_duplicate(self, db):
        User.create_user("alice", "password123")
        assert User.create_user("alice", "otherpass") is False

    def test_find_by_username_exists(self, db):
        User.create_user("alice", "password123")
        user = User.find_by_username("alice")
        assert user is not None
        assert user.username == "alice"

    def test_find_by_username_not_found(self, db):
        assert User.find_by_username("nobody") is None

    def test_find_by_id(self, db):
        User.create_user("alice", "password123")
        created = User.find_by_username("alice")
        assert created is not None and created.id is not None
        found = User.find_by_id(created.id)
        assert found is not None
        assert found.username == "alice"

    def test_find_by_id_not_found(self, db):
        assert User.find_by_id(9999) is None


class TestVerifyPassword:
    def test_correct_password(self):
        h = _ph.hash("secret")
        assert User.verify_password(h, "secret") is True

    def test_wrong_password(self):
        h = _ph.hash("secret")
        assert User.verify_password(h, "wrong") is False

    def test_invalid_hash(self):
        assert User.verify_password("not-a-valid-hash", "password") is False


class TestUpdateUsername:
    def test_update_success(self, db):
        User.create_user("alice", "password123")
        user = User.find_by_username("alice")
        assert user is not None and user.id is not None
        assert User.update_username(user.id, "alice_new") is True
        assert User.find_by_username("alice_new") is not None
        assert User.find_by_username("alice") is None

    def test_update_password(self, db):
        User.create_user("alice", "password123")
        user = User.find_by_username("alice")
        assert user is not None and user.id is not None
        new_hash = _ph.hash("newpass456")
        assert User.update_password(user.id, new_hash) is True
        updated = User.find_by_username("alice")
        assert updated is not None
        assert User.verify_password(updated.password_hash or "", "newpass456") is True
