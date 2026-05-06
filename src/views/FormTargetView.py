from typing import Optional


class FormTargetView:

    def __init__(
        self,
        controller: Optional['TargetEmisiController'] = None,
        inputNilaiTarget: Optional[float] = None,
        inputSatuan: Optional[str] = None,
        inputTahun: Optional[int] = None
    ):
        self._controller = controller
        self._inputNilaiTarget = inputNilaiTarget
        self._inputSatuan = inputSatuan
        self._inputTahun = inputTahun

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value):
        self._controller = value

    @property
    def inputNilaiTarget(self):
        return self._inputNilaiTarget

    @inputNilaiTarget.setter
    def inputNilaiTarget(self, value):
        self._inputNilaiTarget = value

    @property
    def inputSatuan(self):
        return self._inputSatuan

    @inputSatuan.setter
    def inputSatuan(self, value):
        self._inputSatuan = value

    @property
    def inputTahun(self):
        return self._inputTahun

    @inputTahun.setter
    def inputTahun(self, value):
        self._inputTahun = value

    def tampilkan(self) -> None:
        pass

    def fillForm(self, targetData: 'TargetEmisi') -> None:
        pass

    def simpanForm(self) -> None:
        pass

    def tampilkanError(self, pesan: str) -> None:
        pass

    def tampilkanSukses(self) -> None:
        pass