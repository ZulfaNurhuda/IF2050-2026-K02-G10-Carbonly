from typing import Optional


class TargetEmisi:

    def __init__(
        self,
        id: Optional[int] = None,
        nilaiTarget: Optional[float] = None,
        satuan: Optional[str] = None,
        tahun: Optional[int] = None
    ):
        self._id = id
        self._nilaiTarget = nilaiTarget
        self._satuan = satuan
        self._tahun = tahun

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def nilaiTarget(self) -> float:
        return self._nilaiTarget

    @nilaiTarget.setter
    def nilaiTarget(self, value: float):
        self._nilaiTarget = value

    @property
    def satuan(self) -> str:
        return self._satuan

    @satuan.setter
    def satuan(self, value: str):
        self._satuan = value

    @property
    def tahun(self) -> int:
        return self._tahun

    @tahun.setter
    def tahun(self, value: int):
        self._tahun = value

    def ubah(self, data: 'TargetEmisi') -> None:
        pass

    def validasiInput(self) -> bool:
        pass