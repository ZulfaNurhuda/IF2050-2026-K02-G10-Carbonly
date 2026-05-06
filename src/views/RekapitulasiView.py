from typing import Optional
from datetime import datetime


class RekapitulasiView:

    def __init__(
        self,
        controller: Optional['RekapitulasiController'] = None,
        tanggalMulai: Optional[datetime] = None,
        tanggalAkhir: Optional[datetime] = None
    ):
        self._controller = controller
        self._tanggalMulai = tanggalMulai
        self._tanggalAkhir = tanggalAkhir

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value):
        self._controller = value

    @property
    def tanggalMulai(self):
        return self._tanggalMulai

    @tanggalMulai.setter
    def tanggalMulai(self, value):
        self._tanggalMulai = value

    @property
    def tanggalAkhir(self):
        return self._tanggalAkhir

    @tanggalAkhir.setter
    def tanggalAkhir(self, value):
        self._tanggalAkhir = value

    def tampilkan(self) -> None:
        pass

    def pilihRentang(self, tanggalMulai: datetime, tanggalAkhir: datetime) -> None:
        pass

    def tunjukkanRekapitulasi(self, data: object) -> None:
        pass

    def tunjukkanKosong(self) -> None:
        pass