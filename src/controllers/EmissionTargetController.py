from datetime import datetime
from typing import Optional, Tuple

from src.models.EmissionTarget import EmissionTarget


class EmissionTargetController:
    @staticmethod
    def get_target() -> Optional[EmissionTarget]:
        return EmissionTarget.get()

    @staticmethod
    def save_target(data: EmissionTarget) -> Tuple[bool, str]:
        if not data.is_valid():
            return False, "Nilai target tidak valid. Pastikan nilainya lebih dari 0."

        existing = EmissionTarget.get()
        if existing is None:
            data.year = data.year or datetime.now().year
            EmissionTarget.insert(data)
        else:
            existing.update_from(data)
            EmissionTarget.update(existing)

        return True, ""
