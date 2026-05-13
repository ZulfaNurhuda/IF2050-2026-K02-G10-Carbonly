from src.models.EmissionTarget import EmissionTarget


class TestIsValid:
    def test_valid(self):
        target = EmissionTarget(target_value=10.0, unit="kg CO2")
        assert target.is_valid() is True

    def test_zero_value(self):
        target = EmissionTarget(target_value=0.0, unit="kg CO2")
        assert target.is_valid() is False

    def test_negative_value(self):
        target = EmissionTarget(target_value=-1.0, unit="kg CO2")
        assert target.is_valid() is False

    def test_none_value(self):
        target = EmissionTarget(unit="kg CO2")
        assert target.is_valid() is False

    def test_empty_unit(self):
        target = EmissionTarget(target_value=10.0, unit="")
        assert target.is_valid() is False

    def test_whitespace_unit(self):
        target = EmissionTarget(target_value=10.0, unit="   ")
        assert target.is_valid() is False


class TestUpdateFrom:
    def test_updates_all_non_none_fields(self):
        source = EmissionTarget(target_value=20.0, unit="kg", year=2024)
        target = EmissionTarget(target_value=10.0, unit="ton", year=2023)
        target.update_from(source)
        assert target.target_value == 20.0
        assert target.unit == "kg"
        assert target.year == 2024

    def test_skips_none_fields(self):
        source = EmissionTarget(target_value=None, unit=None, year=None)
        target = EmissionTarget(target_value=10.0, unit="ton", year=2023)
        target.update_from(source)
        assert target.target_value == 10.0
        assert target.unit == "ton"
        assert target.year == 2023

    def test_partial_update(self):
        source = EmissionTarget(target_value=50.0, unit=None, year=None)
        target = EmissionTarget(target_value=10.0, unit="ton", year=2023)
        target.update_from(source)
        assert target.target_value == 50.0
        assert target.unit == "ton"
        assert target.year == 2023
