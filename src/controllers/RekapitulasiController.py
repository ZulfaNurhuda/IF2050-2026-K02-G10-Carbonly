# ruff: noqa
# flake8: noqa
# mypy: ignore-errors
from datetime import datetime
from typing import List, TYPE_CHECKING
from src.controllers.LogAktivitasController import LogAktivitasController

if TYPE_CHECKING:
    from src.models.LogAktivitas import LogAktivitas


class RekapitulasiController:
    def __init__(self):
        self._logAktivitasController = LogAktivitasController()
        self._targetEmisiController = None

    @property
    def logAktivitasController(self):
        return self._logAktivitasController

    @logAktivitasController.setter
    def logAktivitasController(self, value):
        self._logAktivitasController = value

    @property
    def targetEmisiController(self):
        return self._targetEmisiController

    @targetEmisiController.setter
    def targetEmisiController(self, value):
        self._targetEmisiController = value

    def dapatkanRekapitulasi(self, tanggalMulai: datetime, tanggalAkhir: datetime) -> object:
        # Mengambil daftar log dari Controller lain
        daftar_log = self.logAktivitasController.dapatkanLogRentang(tanggalMulai, tanggalAkhir)
        total_emisi = self.hitungTotalEmisi(daftar_log) if daftar_log else 0.0

        target_emisi = 0.0
        if self.targetEmisiController:
            target = self.targetEmisiController.dapatkanTarget()
            target_emisi = target.nilaiTarget if target and target.nilaiTarget is not None else 0.0

        hasil = {
            "total_emisi": total_emisi,
            "target_emisi": target_emisi,
            "log": daftar_log if daftar_log else []
        }

        # Jika rentang lebih dari 1 hari (contoh: mingguan), buat data grafik
        delta_hari = (tanggalAkhir - tanggalMulai).days
        if delta_hari > 0:
            from datetime import timedelta
            emisi_per_hari = []
            for i in range(delta_hari + 1):
                tgl_hari_ini = tanggalMulai + timedelta(days=i)
                log_hari_ini = [log for log in (daftar_log or [])
                                if hasattr(log, 'tanggal') and log.tanggal and log.tanggal.date() == tgl_hari_ini.date()]
                total_hari_ini = self.hitungTotalEmisi(log_hari_ini)
                emisi_per_hari.append((tgl_hari_ini, total_hari_ini))
            hasil["emisi_per_hari"] = emisi_per_hari

        return hasil

    def hitungTotalEmisi(self, daftarLog: List["LogAktivitas"]) -> float:
        if not daftarLog:
            return 0.0
        return sum(log.totalEmisi for log in daftarLog if log.totalEmisi is not None)
