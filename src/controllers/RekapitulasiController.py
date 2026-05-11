from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.LogAktivitas import LogAktivitas


class RekapitulasiController:
    def __init__(self):
        self._logAktivitasController = None
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

    def dapatkanRekapitulasi(
        self, tanggalMulai: datetime, tanggalAkhir: datetime
    ) -> object:
        if not self.logAktivitasController or not self.targetEmisiController:
            return {"total_emisi": 0.0, "target_emisi": 0.0}

        daftar_log = self.logAktivitasController.dapatkanLogRentang(tanggalMulai, tanggalAkhir)
        total_emisi = self.hitungTotalEmisi(daftar_log) if daftar_log else 0.0
        
        target = self.targetEmisiController.dapatkanTarget()
        target_emisi = target.nilaiTarget if target and target.nilaiTarget is not None else 0.0
        
        return {
            "total_emisi": total_emisi,
            "target_emisi": target_emisi
        }

    def hitungTotalEmisi(self, daftarLog: List["LogAktivitas"]) -> float:
        if not daftarLog:
            return 0.0
        return sum(log.totalEmisi for log in daftarLog if log.totalEmisi is not None)
