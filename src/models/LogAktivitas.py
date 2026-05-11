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
        totalEmisi: Optional[float] = None,
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

    def ubah(self, data: "LogAktivitas") -> None:
        self._tanggal = data._tanggal
        self._kategori = data._kategori
        self._nilaiAktivitas = data._nilaiAktivitas
        self._satuanAktivitas = data._satuanAktivitas
        self._totalEmisi = data._totalEmisi

    def validasiInput(self) -> bool:
        if self._tanggal is None:
            return False
        if not self._kategori or not self._kategori.strip():
            return False
        if self._nilaiAktivitas is None or self._nilaiAktivitas <= 0:
            return False
        if not self._satuanAktivitas or not self._satuanAktivitas.strip():
            return False
        return True

    def hitungEmisi(self, koefisien: "KoefisienEmisi") -> None:
        if koefisien is not None and self._nilaiAktivitas is not None:
            self._totalEmisi = self._nilaiAktivitas * koefisien.nilaiKoefisien
