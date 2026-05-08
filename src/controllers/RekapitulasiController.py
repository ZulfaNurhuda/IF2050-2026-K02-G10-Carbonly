# ruff: noqa
# flake8: noqa
# mypy: ignore-errors
from datetime import datetime
from typing import List


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
        pass

    def hitungTotalEmisi(self, daftarLog: List["LogAktivitas"]) -> float:
        pass
