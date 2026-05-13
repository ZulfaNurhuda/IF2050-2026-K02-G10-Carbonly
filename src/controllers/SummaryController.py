from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Dict, List

from src.controllers.ActivityLogController import ActivityLogController
from src.controllers.EmissionTargetController import EmissionTargetController

if TYPE_CHECKING:
    from src.models.ActivityLog import ActivityLog


class SummaryController:
    @staticmethod
    def get_summary(start_date: datetime, end_date: datetime) -> Dict:
        logs: List["ActivityLog"] = ActivityLogController.get_logs_in_range(
            start_date, end_date
        )
        total_emission = SummaryController.calculate_total_emission(logs)

        target = EmissionTargetController.get_target()
        target_emission = (
            target.target_value
            if target and target.target_value is not None
            else 0.0
        )

        result: Dict = {
            "total_emission": total_emission,
            "target_emission": target_emission,
            "logs": logs,
        }

        delta_days = (end_date - start_date).days
        if delta_days > 0:
            daily_emissions = []
            for i in range(delta_days + 1):
                day = start_date + timedelta(days=i)
                day_logs = [
                    log for log in logs
                    if log.date and log.date.date() == day.date()
                ]
                daily_emissions.append(
                    (day, SummaryController.calculate_total_emission(day_logs))
                )
            result["daily_emissions"] = daily_emissions

        return result

    @staticmethod
    def calculate_total_emission(logs: List["ActivityLog"]) -> float:
        if not logs:
            return 0.0
        return sum(
            log.total_emission for log in logs if log.total_emission is not None
        )
