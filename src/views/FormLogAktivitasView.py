# ruff: noqa
# flake8: noqa
# mypy: ignore-errors
from datetime import datetime
from typing import Optional

from PyQt6.QtCore import Qt, QDate, QTimer, pyqtSignal
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFormLayout,
    QWidget,
)
from qfluentwidgets import (
    ComboBox,
    PushButton,
    TitleLabel,
    BodyLabel,
    InfoBar,
    InfoBarPosition,
    CalendarPicker,
    DoubleSpinBox,
    FluentIcon,
    MessageBoxBase,
    setFont,
    PrimaryPushButton,
)

from src.controllers.LogAktivitasController import LogAktivitasController
from src.models.LogAktivitas import LogAktivitas


SATUAN_MAP = {
    "Transportasi": "km",
    "Listrik": "kWh",
    "Gas Alam": "m³",
    "Makanan": "kg",
    "Sampah": "kg",
}

KATEGORI_LIST = [f"{k} ({v})" for k, v in SATUAN_MAP.items()]


class FormLogAktivitasView(MessageBoxBase):
    logDisimpan = pyqtSignal()

    def __init__(
        self,
        controller: Optional[LogAktivitasController] = None,
        logTerpilih: Optional[LogAktivitas] = None,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self._controller = controller or LogAktivitasController()
        self._logTerpilih = logTerpilih

        self.setObjectName("form-log-aktivitas-dialog")
        self.setWindowTitle("Log Aktivitas Karbon")

        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.buttonGroup.setFixedHeight(0)

        self._buatWidget()
        self._buatLayout()
        self._hubungkanSinyal()

        self.widget.setMinimumWidth(460)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        if self.parent():
            QTimer.singleShot(0, self._adjust_geometry)

    def _adjust_geometry(self) -> None:
        if self.parent() and hasattr(self.parent(), "width"):
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())

    @property
    def controller(self) -> LogAktivitasController:
        return self._controller

    @controller.setter
    def controller(self, value: LogAktivitasController):
        self._controller = value

    @property
    def logTerpilih(self) -> Optional[LogAktivitas]:
        return self._logTerpilih

    @logTerpilih.setter
    def logTerpilih(self, value: Optional[LogAktivitas]):
        self._logTerpilih = value

    @staticmethod
    def _parseKategori(displayText: str) -> str:
        return displayText.split(" (")[0]

    @property
    def inputKategori(self) -> Optional[str]:
        text = self._cbKategori.currentText()
        return self._parseKategori(text) if text else None

    @property
    def inputTanggal(self) -> Optional[datetime]:
        qdate: QDate = self._datePicker.getDate()
        if qdate.isValid():
            return datetime(qdate.year(), qdate.month(), qdate.day())
        return None

    @property
    def inputBesaran(self) -> Optional[float]:
        v = self._spinNilai.value()
        return v if v > 0 else None

    @property
    def inputSatuan(self) -> Optional[str]:
        kategori = self.inputKategori
        return SATUAN_MAP.get(kategori) if kategori else None

    def _buatWidget(self):
        self._lblJudul = TitleLabel("Catat Aktivitas Karbon")
        setFont(self._lblJudul, 18)

        self._lblKategori = BodyLabel("Kategori Aktivitas")
        self._cbKategori = ComboBox()
        self._cbKategori.addItems(KATEGORI_LIST)

        self._lblTanggal = BodyLabel("Tanggal")
        self._datePicker = CalendarPicker()
        self._datePicker.setDate(QDate.currentDate())

        self._lblNilai = BodyLabel("Besaran Aktivitas")
        self._spinNilai = DoubleSpinBox()
        self._spinNilai.setRange(0.01, 999_999.99)
        self._spinNilai.setDecimals(2)
        self._spinNilai.setSingleStep(1.0)

        self._btnSimpan = PrimaryPushButton(FluentIcon.SAVE, "Simpan")
        self._btnBatal = PushButton(FluentIcon.CLOSE, "Batal")
        self._btnSimpan.setFixedWidth(120)
        self._btnBatal.setFixedWidth(120)

    def _buatLayout(self):
        formLayout = QFormLayout()
        formLayout.setSpacing(14)
        formLayout.setContentsMargins(0, 0, 0, 0)
        formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        formLayout.addRow(self._lblKategori, self._cbKategori)
        formLayout.addRow(self._lblTanggal, self._datePicker)
        formLayout.addRow(self._lblNilai, self._spinNilai)

        btnLayout = QHBoxLayout()
        btnLayout.addStretch()
        btnLayout.addWidget(self._btnBatal)
        btnLayout.addWidget(self._btnSimpan)

        self.viewLayout.setContentsMargins(32, 28, 32, 24)
        self.viewLayout.setSpacing(20)
        self.viewLayout.addWidget(self._lblJudul)
        self.viewLayout.addLayout(formLayout)
        self.viewLayout.addSpacing(8)
        self.viewLayout.addLayout(btnLayout)

    def _hubungkanSinyal(self):
        self._btnSimpan.clicked.connect(self.simpanForm)
        self._btnBatal.clicked.connect(self.reject)

    def _resetForm(self):
        self._logTerpilih = None
        self._cbKategori.setCurrentIndex(0)
        self._datePicker.setDate(QDate.currentDate())
        self._spinNilai.setValue(0.0)
        self._lblJudul.setText("Catat Aktivitas Karbon")

    def tampilkan(self) -> None:
        self._controller.dapatkanDaftarLog()
        self.exec()

    def fillForm(self, logData: LogAktivitas) -> None:
        self._logTerpilih = logData
        self._lblJudul.setText("Edit Aktivitas Karbon")

        display_text = f"{logData.kategori or ''} ({logData.satuanAktivitas or ''})"
        idx = self._cbKategori.findText(display_text)
        self._cbKategori.setCurrentIndex(idx if idx >= 0 else 0)

        if logData.tanggal:
            qd = QDate(logData.tanggal.year, logData.tanggal.month, logData.tanggal.day)
            self._datePicker.setDate(qd)

        self._spinNilai.setValue(logData.nilaiAktivitas or 0.0)

        ok = self._controller.ubahLog(logData)
        if not ok:
            self.tampilkanError("Data log tidak valid untuk diedit.")

    def simpanForm(self) -> None:
        data = LogAktivitas(
            id=self._logTerpilih.id if self._logTerpilih else None,
            tanggal=self.inputTanggal,
            kategori=self.inputKategori,
            nilaiAktivitas=self.inputBesaran,
            satuanAktivitas=self.inputSatuan,
        )

        ok = self._controller.simpanLog(data)
        if ok:
            self.tampilkanSukses()
            self.logDisimpan.emit()
            self._resetForm()
            self.accept()
        else:
            self.tampilkanError(
                "Pastikan semua field terisi dan besaran aktivitas lebih dari 0."
            )

    def tampilkanError(self, pesan: str) -> None:
        InfoBar.error(
            title="Gagal Menyimpan",
            content=pesan,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=4000,
            position=InfoBarPosition.TOP,
            parent=self,
        )

    def tampilkanSukses(self) -> None:
        InfoBar.success(
            title="Berhasil Disimpan",
            content="Log aktivitas karbon berhasil dicatat.",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=3000,
            position=InfoBarPosition.TOP,
            parent=self.parent(),
        )
