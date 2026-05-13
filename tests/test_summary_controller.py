from src.controllers.SummaryController import SummaryController
from src.models.ActivityLog import ActivityLog


class TestCalculateTotalEmission:
    def test_empty_list(self):
        assert SummaryController.calculate_total_emission([]) == 0.0

    def test_single_log(self):
        logs = [ActivityLog(total_emission=5.0)]
        assert SummaryController.calculate_total_emission(logs) == 5.0

    def test_multiple_logs(self):
        logs = [
            ActivityLog(total_emission=5.0),
            ActivityLog(total_emission=3.0),
            ActivityLog(total_emission=2.0),
        ]
        assert SummaryController.calculate_total_emission(logs) == 10.0

    def test_skips_none_emission(self):
        logs = [
            ActivityLog(total_emission=5.0),
            ActivityLog(total_emission=None),
            ActivityLog(total_emission=3.0),
        ]
        assert SummaryController.calculate_total_emission(logs) == 8.0

    def test_all_none_emission(self):
        logs = [ActivityLog(total_emission=None), ActivityLog(total_emission=None)]
        assert SummaryController.calculate_total_emission(logs) == 0.0
