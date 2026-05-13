import sqlite3
from typing import Optional

from src.services.AuthService import AuthService
from src.services.DBContext import DBContext


class EmissionTarget:
    def __init__(
        self,
        id: Optional[int] = None,
        target_value: Optional[float] = None,
        unit: Optional[str] = None,
        year: Optional[int] = None,
    ) -> None:
        self._id = id
        self._target_value = target_value
        self._unit = unit
        self._year = year

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        self._id = value

    @property
    def target_value(self) -> Optional[float]:
        return self._target_value

    @target_value.setter
    def target_value(self, value: Optional[float]) -> None:
        self._target_value = value

    @property
    def unit(self) -> Optional[str]:
        return self._unit

    @unit.setter
    def unit(self, value: Optional[str]) -> None:
        self._unit = value

    @property
    def year(self) -> Optional[int]:
        return self._year

    @year.setter
    def year(self, value: Optional[int]) -> None:
        self._year = value

    def update_from(self, data: "EmissionTarget") -> None:
        if data.target_value is not None:
            self._target_value = data.target_value
        if data.unit is not None:
            self._unit = data.unit
        if data.year is not None:
            self._year = data.year

    def is_valid(self) -> bool:
        if self._target_value is None or self._target_value <= 0:
            return False
        if not self._unit or not self._unit.strip():
            return False
        return True

    @staticmethod
    def _current_user_id() -> Optional[int]:
        user = AuthService.get_current_user()
        return user.id if user else None

    @staticmethod
    def create_table() -> None:
        try:
            with DBContext.connect() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS target_emisi (
                        id           INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id      INTEGER REFERENCES users(id),
                        nilai_target REAL    NOT NULL,
                        satuan       TEXT,
                        tahun        INTEGER NOT NULL
                    )
                """)
        except sqlite3.Error:
            pass

    @staticmethod
    def get() -> Optional["EmissionTarget"]:
        user_id = EmissionTarget._current_user_id()
        if user_id is None:
            return None
        try:
            with DBContext.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, nilai_target, satuan, tahun "
                    "FROM target_emisi WHERE user_id = ? "
                    "ORDER BY tahun DESC, id DESC LIMIT 1",
                    (user_id,),
                )
                row = cursor.fetchone()
            if row:
                return EmissionTarget(
                    id=row[0],
                    target_value=row[1],
                    unit=row[2],
                    year=row[3],
                )
            return None
        except sqlite3.Error:
            return None

    @staticmethod
    def insert(target: "EmissionTarget") -> "EmissionTarget":
        user_id = EmissionTarget._current_user_id()
        if user_id is None:
            return target
        try:
            with DBContext.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO target_emisi (user_id, nilai_target, satuan, tahun) "
                    "VALUES (?, ?, ?, ?)",
                    (user_id, target.target_value, target.unit, target.year),
                )
                target.id = cursor.lastrowid
        except sqlite3.Error:
            pass
        return target

    @staticmethod
    def update(target: "EmissionTarget") -> None:
        user_id = EmissionTarget._current_user_id()
        if user_id is None:
            return
        try:
            with DBContext.connect() as conn:
                conn.execute(
                    "UPDATE target_emisi SET nilai_target = ?, satuan = ?, tahun = ? "
                    "WHERE id = ? AND user_id = ?",
                    (target.target_value, target.unit, target.year, target.id, user_id),
                )
        except sqlite3.Error:
            pass

    @staticmethod
    def save(target: "EmissionTarget") -> "EmissionTarget":
        if target.id is None:
            return EmissionTarget.insert(target)
        EmissionTarget.update(target)
        return target
