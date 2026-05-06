from datetime import datetime
from typing import Optional


class LogAktivitas:

    def __init__(
        self,
        id: Optional[int] = None,
        tanggal: Optional[datetime] = None,
        kategori: Optional[str] = None,
        nilaiAktivitas: Optional[float] = None,
        satuanAktivitas: Optional[str] = None,
        totalEmisi: Optional[float] = None
    ):
        self._id = id
        self._tanggal = tanggal
        self._kategori = kategori
        self._nilaiAktivitas = nilaiAktivitas
        self._satuanAktivitas = satuanAktivitas
        self._totalEmisi = totalEmisi

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def tanggal(self) -> datetime:
        return self._tanggal

    @tanggal.setter
    def tanggal(self, value: datetime):
        self._tanggal = value

    @property
    def kategori(self) -> str:
        return self._kategori

    @kategori.setter
    def kategori(self, value: str):
        self._kategori = value

    @property
    def nilaiAktivitas(self) -> float:
        return self._nilaiAktivitas

    @nilaiAktivitas.setter
    def nilaiAktivitas(self, value: float):
        self._nilaiAktivitas = value

    @property
    def satuanAktivitas(self) -> str:
        return self._satuanAktivitas

    @satuanAktivitas.setter
    def satuanAktivitas(self, value: str):
        self._satuanAktivitas = value

    @property
    def totalEmisi(self) -> float:
        return self._totalEmisi

    @totalEmisi.setter
    def totalEmisi(self, value: float):
        self._totalEmisi = value

    def ubah(self, data: 'LogAktivitas') -> None:
        pass

    def validasiInput(self) -> bool:
        pass

    def hitungEmisi(self, koefisien: 'KoefisienEmisi') -> None:
        pass