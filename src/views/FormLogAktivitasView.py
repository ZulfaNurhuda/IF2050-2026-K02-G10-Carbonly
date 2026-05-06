from typing import Optional


class FormLogAktivitasView:
    def __init__(
        self,
        controller: Optional["LogAktivitasController"] = None,
        logTerpilih: Optional["LogAktivitas"] = None,
        inputKategori: Optional[str] = None,
        inputTanggal: Optional["datetime"] = None,
        inputBesaran: Optional[float] = None,
        inputSatuan: Optional[str] = None,
    ):
        self._controller = controller
        self._logTerpilih = logTerpilih
        self._inputKategori = inputKategori
        self._inputTanggal = inputTanggal
        self._inputBesaran = inputBesaran
        self._inputSatuan = inputSatuan

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value):
        self._controller = value

    @property
    def logTerpilih(self):
        return self._logTerpilih

    @logTerpilih.setter
    def logTerpilih(self, value):
        self._logTerpilih = value

    @property
    def inputKategori(self):
        return self._inputKategori

    @inputKategori.setter
    def inputKategori(self, value):
        self._inputKategori = value

    @property
    def inputTanggal(self):
        return self._inputTanggal

    @inputTanggal.setter
    def inputTanggal(self, value):
        self._inputTanggal = value

    @property
    def inputBesaran(self):
        return self._inputBesaran

    @inputBesaran.setter
    def inputBesaran(self, value):
        self._inputBesaran = value

    @property
    def inputSatuan(self):
        return self._inputSatuan

    @inputSatuan.setter
    def inputSatuan(self, value):
        self._inputSatuan = value

    def tampilkan(self) -> None:
        pass

    def fillForm(self, targetData: "TargetEmisi") -> None:
        pass

    def simpanForm(self) -> None:
        pass

    def tampilkanError(self, pesan: str) -> None:
        pass

    def tampilkanSukses(self) -> None:
        pass
