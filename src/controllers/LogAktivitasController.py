# ruff: noqa
# flake8: noqa
# mypy: ignore-errors
from datetime import datetime
from typing import List


class LogAktivitasController:
    def __init__(self):
        self._logAktivitas = None

    @property
    def logAktivitas(self):
        return self._logAktivitas

    @logAktivitas.setter
    def logAktivitas(self, value):
        self._logAktivitas = value

    def dapatkanDaftarLog(self) -> List["LogAktivitas"]:
        pass

    def tambahLog(self, data: "LogAktivitas") -> None:
        pass

    def ubahLog(self, data: "LogAktivitas") -> None:
        pass

    def simpanLog(self, data: "LogAktivitas") -> None:
        pass

    def hapusLog(self, id: int) -> None:
        pass

    def dapatkanLogRentang(
        self, tanggalMulai: datetime, tanggalAkhir: datetime
    ) -> List["LogAktivitas"]:
        pass
