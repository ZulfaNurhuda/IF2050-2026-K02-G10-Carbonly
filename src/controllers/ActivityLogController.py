import sqlite3
from datetime import datetime
from typing import List, Optional

from src.models.ActivityLog import ActivityLog
from src.models.EmissionCoefficient import EmissionCoefficient
from src.services.AuthService import AuthService
from src.services.DBContext import DBContext


class ActivityLogController:
    @staticmethod
    def _current_user_id() -> Optional[int]:
        user = AuthService.get_current_user()
        return user.id if user else None

    @staticmethod
    def initialize_database() -> None:
        try:
            with DBContext.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS log_aktivitas (
                        id               INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id          INTEGER REFERENCES users(id),
                        tanggal          TEXT    NOT NULL,
                        kategori         TEXT    NOT NULL,
                        nilai_aktivitas  REAL    NOT NULL,
                        satuan_aktivitas TEXT    NOT NULL,
                        total_emisi      REAL
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS koefisien_emisi (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        kategori        TEXT    NOT NULL UNIQUE,
                        nilai_koefisien REAL    NOT NULL,
                        satuan          TEXT    NOT NULL
                    )
                """)
                cursor.execute("SELECT COUNT(*) FROM koefisien_emisi")
                if cursor.fetchone()[0] == 0:
                    default_coefficients = [
                        ("Transportasi", 0.21, "kg CO2e/km"),
                        ("Listrik", 0.87, "kg CO2e/kWh"),
                        ("Gas Alam", 2.04, "kg CO2e/m³"),
                        ("Makanan", 0.50, "kg CO2e/kg"),
                        ("Sampah", 0.44, "kg CO2e/kg"),
                    ]
                    cursor.executemany(
                        "INSERT INTO koefisien_emisi "
                        "(kategori, nilai_koefisien, satuan) VALUES (?, ?, ?)",
                        default_coefficients,
                    )
        except sqlite3.Error:
            pass

    @staticmethod
    def _row_to_log(row: sqlite3.Row) -> ActivityLog:
        return ActivityLog(
            id=row["id"],
            date=datetime.fromisoformat(row["tanggal"]),
            category=row["kategori"],
            activity_value=row["nilai_aktivitas"],
            activity_unit=row["satuan_aktivitas"],
            total_emission=row["total_emisi"],
        )

    @staticmethod
    def get_all_logs() -> List[ActivityLog]:
        user_id = ActivityLogController._current_user_id()
        if user_id is None:
            return []
        try:
            with DBContext.connect() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, tanggal, kategori, nilai_aktivitas, "
                    "satuan_aktivitas, total_emisi "
                    "FROM log_aktivitas WHERE user_id = ? ORDER BY tanggal DESC",
                    (user_id,),
                )
                rows = cursor.fetchall()
                return [ActivityLogController._row_to_log(r) for r in rows]
        except sqlite3.Error:
            return []

    @staticmethod
    def get_logs_in_range(
        start_date: datetime, end_date: datetime
    ) -> List[ActivityLog]:
        user_id = ActivityLogController._current_user_id()
        if user_id is None:
            return []
        try:
            with DBContext.connect() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, tanggal, kategori, nilai_aktivitas, "
                    "satuan_aktivitas, total_emisi "
                    "FROM log_aktivitas "
                    "WHERE user_id = ? AND tanggal BETWEEN ? AND ? "
                    "ORDER BY tanggal DESC",
                    (user_id, start_date.isoformat(), end_date.isoformat()),
                )
                rows = cursor.fetchall()
                return [ActivityLogController._row_to_log(r) for r in rows]
        except sqlite3.Error:
            return []

    @staticmethod
    def save_log(data: ActivityLog) -> bool:
        if not data.is_valid():
            return False
        user_id = ActivityLogController._current_user_id()
        if user_id is None:
            return False
        coefficient: Optional[EmissionCoefficient] = (
            EmissionCoefficient.find_by_category(data.category or "")
        )
        data.calculate_emission(coefficient)
        try:
            with DBContext.connect() as conn:
                cursor = conn.cursor()
                if data.id is None:
                    cursor.execute(
                        "INSERT INTO log_aktivitas (user_id, tanggal, kategori, "
                        "nilai_aktivitas, satuan_aktivitas, total_emisi) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            user_id,
                            data.date.isoformat() if data.date else "",
                            data.category,
                            data.activity_value,
                            data.activity_unit,
                            data.total_emission,
                        ),
                    )
                    data.id = cursor.lastrowid
                else:
                    cursor.execute(
                        "UPDATE log_aktivitas SET "
                        "tanggal = ?, kategori = ?, nilai_aktivitas = ?, "
                        "satuan_aktivitas = ?, total_emisi = ? "
                        "WHERE id = ? AND user_id = ?",
                        (
                            data.date.isoformat() if data.date else "",
                            data.category,
                            data.activity_value,
                            data.activity_unit,
                            data.total_emission,
                            data.id,
                            user_id,
                        ),
                    )
            return True
        except sqlite3.Error:
            return False

    @staticmethod
    def delete_log(log_id: int) -> None:
        user_id = ActivityLogController._current_user_id()
        if user_id is None:
            return
        try:
            with DBContext.connect() as conn:
                conn.execute(
                    "DELETE FROM log_aktivitas WHERE id = ? AND user_id = ?",
                    (log_id, user_id),
                )
        except sqlite3.Error:
            pass
