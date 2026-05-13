from datetime import datetime
from unittest.mock import MagicMock

from src.models.ActivityLog import ActivityLog


class TestIsValid:
    def test_valid(self):
        log = ActivityLog(
            date=datetime.now(), category="Transport", activity_value=10.0, activity_unit="km"
        )
        assert log.is_valid() is True

    def test_missing_date(self):
        log = ActivityLog(category="Transport", activity_value=10.0, activity_unit="km")
        assert log.is_valid() is False

    def test_empty_category(self):
        log = ActivityLog(
            date=datetime.now(), category="", activity_value=10.0, activity_unit="km"
        )
        assert log.is_valid() is False

    def test_whitespace_category(self):
        log = ActivityLog(
            date=datetime.now(), category="   ", activity_value=10.0, activity_unit="km"
        )
        assert log.is_valid() is False

    def test_zero_activity_value(self):
        log = ActivityLog(
            date=datetime.now(), category="Transport", activity_value=0.0, activity_unit="km"
        )
        assert log.is_valid() is False

    def test_negative_activity_value(self):
        log = ActivityLog(
            date=datetime.now(), category="Transport", activity_value=-5.0, activity_unit="km"
        )
        assert log.is_valid() is False

    def test_none_activity_value(self):
        log = ActivityLog(date=datetime.now(), category="Transport", activity_unit="km")
        assert log.is_valid() is False

    def test_empty_unit(self):
        log = ActivityLog(
            date=datetime.now(), category="Transport", activity_value=10.0, activity_unit=""
        )
        assert log.is_valid() is False

    def test_whitespace_unit(self):
        log = ActivityLog(
            date=datetime.now(), category="Transport", activity_value=10.0, activity_unit="   "
        )
        assert log.is_valid() is False


class TestCalculateEmission:
    def test_with_coefficient(self):
        log = ActivityLog(activity_value=10.0)
        coef = MagicMock()
        coef.coefficient_value = 2.5
        log.calculate_emission(coef)
        assert log.total_emission == 25.0

    def test_with_none_coefficient(self):
        log = ActivityLog(activity_value=10.0, total_emission=99.0)
        log.calculate_emission(None)
        assert log.total_emission == 99.0

    def test_with_zero_coefficient_value(self):
        log = ActivityLog(activity_value=10.0)
        coef = MagicMock()
        coef.coefficient_value = 0.0
        log.calculate_emission(coef)
        assert log.total_emission == 0.0

    def test_with_none_coefficient_value(self):
        log = ActivityLog(activity_value=10.0)
        coef = MagicMock()
        coef.coefficient_value = None
        log.calculate_emission(coef)
        assert log.total_emission == 0.0


class TestUpdateFrom:
    def test_copies_all_fields(self):
        source = ActivityLog(
            date=datetime(2024, 1, 1),
            category="Food",
            activity_value=5.0,
            activity_unit="kg",
            total_emission=3.0,
        )
        target = ActivityLog(id=99)
        target.update_from(source)
        assert target.date == datetime(2024, 1, 1)
        assert target.category == "Food"
        assert target.activity_value == 5.0
        assert target.activity_unit == "kg"
        assert target.total_emission == 3.0
        assert target.id == 99
