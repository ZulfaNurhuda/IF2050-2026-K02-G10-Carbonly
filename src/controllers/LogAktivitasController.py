# ruff: noqa
# flake8: noqa
# mypy: ignore-errors
import sqlite3
from datetime import datetime
from typing import List, Optional

from src.models.KoefisienEmisi import KoefisienEmisi
from src.models.LogAktivitas import LogAktivitas
from src.services.DBContext import DBContext


class LogAktivitasController:
    def __init__(self):
        self._logAktivitas: Optional[LogAktivitas] = None
        self._inisialisasiDatabase()

    @property
    def logAktivitas(self) -> Optional[LogAktivitas]:
        return self._logAktivitas

    @logAktivitas.setter
    def logAktivitas(self, value: Optional[LogAktivitas]):
        self._logAktivitas = value

    def _inisialisasiDatabase(self) -> None:
        with DBContext.connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS log_aktivitas (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    tanggal         TEXT    NOT NULL,
                    kategori        TEXT    NOT NULL,
                    nilai_aktivitas REAL    NOT NULL,
                    satuan_aktivitas TEXT   NOT NULL,
                    total_emisi     REAL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS koefisien_emisi (
                    id               INTEGER PRIMARY KEY AUTOINCREMENT,
                    kategori         TEXT    NOT NULL UNIQUE,
                    nilai_koefisien  REAL    NOT NULL,
                    satuan           TEXT    NOT NULL
                )
            """)

            # Seed data koefisien emisi jika tabel masih kosong
            cursor.execute("SELECT COUNT(*) FROM koefisien_emisi")
            if cursor.fetchone()[0] == 0:
                default_koefisien = [
                    ("Transportasi", 0.21, "kg CO2e/km"),
                    ("Listrik",      0.87, "kg CO2e/kWh"),
                    ("Gas Alam",     2.04, "kg CO2e/m³"),
                    ("Makanan",      0.50, "kg CO2e/kg"),
                    ("Sampah",       0.44, "kg CO2e/kg"),
                ]
                cursor.executemany(
                    "INSERT INTO koefisien_emisi (kategori, nilai_koefisien, satuan) "
                    "VALUES (?, ?, ?)",
                    default_koefisien,
                )


    @staticmethod
    def _rowToLog(row: sqlite3.Row) -> LogAktivitas:
        return LogAktivitas(
            id=row["id"],
            tanggal=datetime.fromisoformat(row["tanggal"]),
            kategori=row["kategori"],
            nilaiAktivitas=row["nilai_aktivitas"],
            satuanAktivitas=row["satuan_aktivitas"],
            totalEmisi=row["total_emisi"],
        )

    def dapatkanDaftarLog(self) -> List[LogAktivitas]:
        with DBContext.connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, tanggal, kategori, nilai_aktivitas, "
                "satuan_aktivitas, total_emisi "
                "FROM log_aktivitas ORDER BY tanggal DESC"
            )
            return [self._rowToLog(row) for row in cursor.fetchall()]

    def tambahLog(self, data: LogAktivitas) -> None:
        self._logAktivitas = data

    def ubahLog(self, data: LogAktivitas) -> bool:
        if not data.validasiInput():
            return False

        koefisien = KoefisienEmisi.dapatkanBerdasarkanKategori(data.kategori)
        if koefisien:
            data.hitungEmisi(koefisien)

        with DBContext.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE log_aktivitas SET "
                "tanggal = ?, kategori = ?, nilai_aktivitas = ?, "
                "satuan_aktivitas = ?, total_emisi = ? "
                "WHERE id = ?",
                (
                    data.tanggal.isoformat(),
                    data.kategori,
                    data.nilaiAktivitas,
                    data.satuanAktivitas,
                    data.totalEmisi,
                    data.id,
                ),
            )
            self._logAktivitas = data
            return True

    def simpanLog(self, data: LogAktivitas) -> bool:
        if not data.validasiInput():
            return False

        koefisien = KoefisienEmisi.dapatkanBerdasarkanKategori(data.kategori)
        data.hitungEmisi(koefisien)

        with DBContext.connect() as conn:
            cursor = conn.cursor()
            if data.id is None:
                cursor.execute(
                    "INSERT INTO log_aktivitas "
                    "(tanggal, kategori, nilai_aktivitas, satuan_aktivitas, total_emisi) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        data.tanggal.isoformat(),
                        data.kategori,
                        data.nilaiAktivitas,
                        data.satuanAktivitas,
                        data.totalEmisi,
                    ),
                )
                data.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE log_aktivitas SET "
                    "tanggal = ?, kategori = ?, nilai_aktivitas = ?, "
                    "satuan_aktivitas = ?, total_emisi = ? "
                    "WHERE id = ?",
                    (
                        data.tanggal.isoformat(),
                        data.kategori,
                        data.nilaiAktivitas,
                        data.satuanAktivitas,
                        data.totalEmisi,
                        data.id,
                    ),
                )
            self._logAktivitas = data
            return True

    def hapusLog(self, id: int) -> None:
        with DBContext.connect() as conn:
            conn.execute("DELETE FROM log_aktivitas WHERE id = ?", (id,))

    def dapatkanLogRentang(
        self, tanggalMulai: datetime, tanggalAkhir: datetime
    ) -> List[LogAktivitas]:
        with DBContext.connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, tanggal, kategori, nilai_aktivitas, "
                "satuan_aktivitas, total_emisi "
                "FROM log_aktivitas "
                "WHERE tanggal BETWEEN ? AND ? "
                "ORDER BY tanggal DESC",
                (tanggalMulai.isoformat(), tanggalAkhir.isoformat()),
            )
            return [self._rowToLog(row) for row in cursor.fetchall()]
