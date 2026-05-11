# ruff: noqa
# flake8: noqa
# mypy: ignore-errors
from datetime import datetime
from typing import Optional

from src.services.DBContext import DBContext


class TargetEmisi:
    def __init__(
        self,
        id: Optional[int] = None,
        nilaiTarget: Optional[float] = None,
        satuan: Optional[str] = None,
        tahun: Optional[int] = None,
    ):
        self._id = id
        self._nilaiTarget = nilaiTarget
        self._satuan = satuan
        self._tahun = tahun

    # ------------------------------------------------------------------ #
    # Properties                                                           #
    # ------------------------------------------------------------------ #

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def nilaiTarget(self) -> Optional[float]:
        return self._nilaiTarget

    @nilaiTarget.setter
    def nilaiTarget(self, value: float):
        self._nilaiTarget = value

    @property
    def satuan(self) -> Optional[str]:
        return self._satuan

    @satuan.setter
    def satuan(self, value: str):
        self._satuan = value

    @property
    def tahun(self) -> Optional[int]:
        return self._tahun

    @tahun.setter
    def tahun(self, value: int):
        self._tahun = value

    # ------------------------------------------------------------------ #
    # Instance methods                                                     #
    # ------------------------------------------------------------------ #

    def ubah(self, data: "TargetEmisi") -> None:
        """Update attributes from another TargetEmisi instance."""
        if data.nilaiTarget is not None:
            self._nilaiTarget = data.nilaiTarget
        if data.satuan is not None:
            self._satuan = data.satuan
        if data.tahun is not None:
            self._tahun = data.tahun

    def validasiInput(self) -> bool:
        """Return True when all required fields are valid."""
        if self._nilaiTarget is None or self._nilaiTarget <= 0:
            return False
        if not self._satuan or not self._satuan.strip():
            return False
        return True

    # ------------------------------------------------------------------ #
    # Static / class-level DB helpers                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def create_table() -> None:
        """Create the target_emisi table if it does not exist."""
        with DBContext.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS target_emisi (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    nilai_target REAL    NOT NULL,
                    satuan  TEXT,
                    tahun   INTEGER NOT NULL
                )
            """)

    @staticmethod
    def get() -> Optional["TargetEmisi"]:
        """Return the most recent target, or None if none exists."""
        with DBContext.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nilai_target, satuan, tahun "
                "FROM target_emisi ORDER BY tahun DESC, id DESC LIMIT 1"
            )
            row = cursor.fetchone()
        if row:
            return TargetEmisi(
                id=row[0],
                nilaiTarget=row[1],
                satuan=row[2],
                tahun=row[3],
            )
        return None

    @staticmethod
    def insert(target: "TargetEmisi") -> "TargetEmisi":
        """Insert a new target row and return it with the generated id."""
        with DBContext.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO target_emisi (nilai_target, satuan, tahun) "
                "VALUES (?, ?, ?)",
                (target.nilaiTarget, target.satuan, target.tahun),
            )
            target.id = cursor.lastrowid
        return target

    @staticmethod
    def update(target: "TargetEmisi") -> None:
        """Overwrite an existing target row identified by id."""
        with DBContext.connect() as conn:
            conn.execute(
                "UPDATE target_emisi SET nilai_target = ?, satuan = ? "
                "WHERE id = ?",
                (target.nilaiTarget, target.satuan, target.id),
            )

    @staticmethod
    def save(target: "TargetEmisi") -> "TargetEmisi":
        """Insert if id is None, otherwise update."""
        if target.id is None:
            return TargetEmisi.insert(target)
        TargetEmisi.update(target)
        return target