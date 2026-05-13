from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.models.EmissionCoefficient import EmissionCoefficient


class ActivityLog:
    def __init__(
        self,
        id: Optional[int] = None,
        date: Optional[datetime] = None,
        category: Optional[str] = None,
        activity_value: Optional[float] = None,
        activity_unit: Optional[str] = None,
        total_emission: Optional[float] = None,
    ) -> None:
        self._id = id
        self._date = date
        self._category = category
        self._activity_value = activity_value
        self._activity_unit = activity_unit
        self._total_emission = total_emission

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        self._id = value

    @property
    def date(self) -> Optional[datetime]:
        return self._date

    @date.setter
    def date(self, value: Optional[datetime]) -> None:
        self._date = value

    @property
    def category(self) -> Optional[str]:
        return self._category

    @category.setter
    def category(self, value: Optional[str]) -> None:
        self._category = value

    @property
    def activity_value(self) -> Optional[float]:
        return self._activity_value

    @activity_value.setter
    def activity_value(self, value: Optional[float]) -> None:
        self._activity_value = value

    @property
    def activity_unit(self) -> Optional[str]:
        return self._activity_unit

    @activity_unit.setter
    def activity_unit(self, value: Optional[str]) -> None:
        self._activity_unit = value

    @property
    def total_emission(self) -> Optional[float]:
        return self._total_emission

    @total_emission.setter
    def total_emission(self, value: Optional[float]) -> None:
        self._total_emission = value

    def update_from(self, data: "ActivityLog") -> None:
        self._date = data._date
        self._category = data._category
        self._activity_value = data._activity_value
        self._activity_unit = data._activity_unit
        self._total_emission = data._total_emission

    def is_valid(self) -> bool:
        if self._date is None:
            return False
        if not self._category or not self._category.strip():
            return False
        if self._activity_value is None or self._activity_value <= 0:
            return False
        if not self._activity_unit or not self._activity_unit.strip():
            return False
        return True

    def calculate_emission(self, coefficient: Optional["EmissionCoefficient"]) -> None:
        if coefficient is not None and self._activity_value is not None:
            coef_val = coefficient.coefficient_value or 0.0
            self._total_emission = self._activity_value * coef_val
