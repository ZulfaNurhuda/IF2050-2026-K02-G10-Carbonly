from typing import List, Optional


class DaftarLogAktivitasView:

    def __init__(
        self,
        controller: Optional['LogAktivitasController'] = None,
        logTerpilih: Optional['LogAktivitas'] = None,
        daftarLog: Optional[List['LogAktivitas']] = None
    ):
        self._controller = controller
        self._logTerpilih = logTerpilih
        self._daftarLog = daftarLog

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
    def daftarLog(self):
        return self._daftarLog

    @daftarLog.setter
    def daftarLog(self, value):
        self._daftarLog = value

    def tampilkan(self) -> None:
        pass

    def pilihLog(self, log: 'LogAktivitas') -> None:
        pass

    def hapusLog(self) -> None:
        pass

    def konfirmasi(self) -> None:
        pass

    def batal(self) -> None:
        pass

    def tutupKonfirmasi(self) -> None:
        pass

    def tunjukkanDaftarLog(self, daftarLog: List['LogAktivitas']) -> None:
        pass

    def tunjukkanKosong(self) -> None:
        pass