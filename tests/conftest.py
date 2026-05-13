import pytest

from src.controllers.ActivityLogController import ActivityLogController
from src.models.EmissionTarget import EmissionTarget
from src.models.User import User
from src.services.AuthService import AuthService
from src.services.DBContext import DBContext


@pytest.fixture
def db(monkeypatch, tmp_path):
    monkeypatch.setattr(DBContext, "_DB_PATH", str(tmp_path / "test.db"))
    User.create_table()
    EmissionTarget.create_table()
    ActivityLogController.initialize_database()
    yield
    AuthService.set_current_user(None)
