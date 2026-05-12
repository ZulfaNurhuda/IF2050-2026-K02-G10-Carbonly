# ruff: noqa
# flake8: noqa
# mypy: ignore-errors
from typing import Optional
import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "carbonly.db")


class KoefisienEmisi:
    def __init__(
        self,
        id: Optional[int] = None,
        kategori: Optional[str] = None,
        nilaiKoefisien: Optional[float] = None,
        satuan: Optional[str] = None,
    ):
        self._id = id
        self._kategori = kategori
        self._nilaiKoefisien = nilaiKoefisien
        self._satuan = satuan

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def kategori(self) -> str:
        return self._kategori

    @kategori.setter
    def kategori(self, value: str):
        self._kategori = value

    @property
    def nilaiKoefisien(self) -> float:
        return self._nilaiKoefisien

    @nilaiKoefisien.setter
    def nilaiKoefisien(self, value: float):
        self._nilaiKoefisien = value

    @property
    def satuan(self) -> str:
        return self._satuan

    @satuan.setter
    def satuan(self, value: str):
        self._satuan = value

    @staticmethod
    def dapatkanBerdasarkanKategori(kategori: str) -> Optional["KoefisienEmisi"]:
        db_path = os.path.abspath(DB_PATH)
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, kategori, nilai_koefisien, satuan "
                "FROM koefisien_emisi WHERE kategori = ?",
                (kategori,),
            )
            row = cursor.fetchone()
            if row:
                return KoefisienEmisi(
                    id=row[0],
                    kategori=row[1],
                    nilaiKoefisien=row[2],
                    satuan=row[3],
                )
            return None
        finally:
            conn.close()
