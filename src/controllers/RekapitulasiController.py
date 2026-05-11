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

    def dapatkanDataHarian(self, tanggal: datetime) -> object:
        if not self.logAktivitasController or not self.targetEmisiController:
            return {"total_emisi": 0.0, "target_emisi": 0.0, "log": []}

        # Mengambil log untuk satu hari penuh
        daftar_log = self.logAktivitasController.dapatkanLogRentang(tanggal, tanggal)
        total_emisi = self.hitungTotalEmisi(daftar_log) if daftar_log else 0.0
        
        target = self.targetEmisiController.dapatkanTarget()
        target_emisi = target.nilaiTarget if target and target.nilaiTarget is not None else 0.0
        
        return {
            "total_emisi": total_emisi,
            "target_emisi": target_emisi,
            "log": daftar_log if daftar_log else []
        }

    def dapatkanDataMingguan(self, tanggal_mulai: datetime, tanggal_akhir: datetime) -> object:
        if not self.logAktivitasController or not self.targetEmisiController:
            return {"total_emisi": 0.0, "target_emisi": 0.0, "emisi_per_hari": []}
            
        daftar_log = self.logAktivitasController.dapatkanLogRentang(tanggal_mulai, tanggal_akhir)
        total_emisi = self.hitungTotalEmisi(daftar_log) if daftar_log else 0.0
        
        target = self.targetEmisiController.dapatkanTarget()
        target_emisi = target.nilaiTarget if target and target.nilaiTarget is not None else 0.0
        
        # Kelompokkan emisi per hari untuk grafik batang (7 hari)
        from datetime import timedelta
        emisi_per_hari = []
        
        # Menghitung selisih hari
        delta = (tanggal_akhir - tanggal_mulai).days
        for i in range(delta + 1):
            tgl_hari_ini = tanggal_mulai + timedelta(days=i)
            # Filter log yang sesuai dengan tgl_hari_ini
            # Asumsi: log.tanggal adalah datetime dan kita bandingkan date-nya
            log_hari_ini = [log for log in (daftar_log or []) 
                            if hasattr(log, 'tanggal') and log.tanggal and log.tanggal.date() == tgl_hari_ini.date()]
            total_hari_ini = self.hitungTotalEmisi(log_hari_ini)
            emisi_per_hari.append((tgl_hari_ini, total_hari_ini))
            
        return {
            "total_emisi": total_emisi,
            "target_emisi": target_emisi,
            "emisi_per_hari": emisi_per_hari
        }

    def hitungTotalEmisi(self, daftarLog: List["LogAktivitas"]) -> float:
        if not daftarLog:
            return 0.0
        return sum(log.totalEmisi for log in daftarLog if log.totalEmisi is not None)
