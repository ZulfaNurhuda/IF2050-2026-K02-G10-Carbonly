from typing import Optional


class KategoriAktivitas:

    def __init__(
        self,
        nama: Optional[str] = None,
        deskripsi: Optional[str] = None
    ):
        self._nama = nama
        self._deskripsi = deskripsi

    @property
    def nama(self) -> str:
        return self._nama

    @nama.setter
    def nama(self, value: str):
        self._nama = value

    @property
    def deskripsi(self) -> str:
        return self._deskripsi

    @deskripsi.setter
    def deskripsi(self, value: str):
        self._deskripsi = value