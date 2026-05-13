import sqlite3
from typing import Optional

from src.services.DBContext import DBContext


class EmissionCoefficient:
    def __init__(
        self,
        id: Optional[int] = None,
        category: Optional[str] = None,
        coefficient_value: Optional[float] = None,
        unit: Optional[str] = None,
    ) -> None:
        self._id = id
        self._category = category
        self._coefficient_value = coefficient_value
        self._unit = unit

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        self._id = value

    @property
    def category(self) -> Optional[str]:
        return self._category

    @category.setter
    def category(self, value: Optional[str]) -> None:
        self._category = value

    @property
    def coefficient_value(self) -> Optional[float]:
        return self._coefficient_value

    @coefficient_value.setter
    def coefficient_value(self, value: Optional[float]) -> None:
        self._coefficient_value = value

    @property
    def unit(self) -> Optional[str]:
        return self._unit

    @unit.setter
    def unit(self, value: Optional[str]) -> None:
        self._unit = value

    @staticmethod
    def find_by_category(category: str) -> Optional["EmissionCoefficient"]:
        try:
            with DBContext.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, kategori, nilai_koefisien, satuan "
                    "FROM koefisien_emisi WHERE kategori = ?",
                    (category,),
                )
                row = cursor.fetchone()
            if row:
                return EmissionCoefficient(
                    id=row[0],
                    category=row[1],
                    coefficient_value=row[2],
                    unit=row[3],
                )
            return None
        except sqlite3.Error:
            return None
