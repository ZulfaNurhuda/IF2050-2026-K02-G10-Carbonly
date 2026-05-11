from datetime import datetime
from typing import Optional

from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QWidget,
    QSizePolicy,
)
from qfluentwidgets import (
    LineEdit,
    ComboBox,
    PushButton,
    TitleLabel,
    BodyLabel,
    InfoBar,
    InfoBarPosition,
    CalendarPicker,
    DoubleSpinBox,
    CardWidget,
    FluentIcon,
    setFont,
    PrimaryPushButton,
)

from src.controllers.LogAktivitasController import LogAktivitasController
from src.models.LogAktivitas import LogAktivitas


# Kategori yang tersedia (harus sesuai dengan data seed di controller)
KATEGORI_LIST = ["Transportasi", "Listrik", "Gas Alam", "Makanan", "Sampah"]
SATUAN_MAP = {
    "Transportasi": "km",
    "Listrik": "kWh",
    "Gas Alam": "m³",
    "Makanan": "kg",
    "Sampah": "kg",
}


class FormLogAktivitasView(QDialog):
    """
    Dialog form untuk menambah atau mengedit satu log aktivitas karbon.

    Dipanggil dari LogAktivitasPage melalui tombol "Tambah Log" atau "Edit".
    Setelah berhasil disimpan, sinyal logDisimpan dikirim ke halaman pemanggil.

    Alur sesuai sequence diagram:
      tampilkan() → fillForm(log) [opt] → ubahLog()
      simpanForm() → simpanLog() → tampilkanSukses() / tampilkanError()
    """

    # Sinyal yang dikirim ke pemanggil setelah log berhasil disimpan
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
        self.setMinimumWidth(460)
        self.setModal(True)

        self._buatWidget()
        self._buatLayout()
        self._hubungkanSinyal()

    # ------------------------------------------------------------------ #
    #  Properties                                                          #
    # ------------------------------------------------------------------ #

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

    @property
    def inputKategori(self) -> Optional[str]:
        return self._cbKategori.currentText() or None

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
        return self._cbSatuan.currentText() or None

    # ------------------------------------------------------------------ #
    #  Widget & Layout construction                                        #
    # ------------------------------------------------------------------ #

    def _buatWidget(self):
        """Membuat semua widget input."""
        _white = "color: white;"

        # Judul dialog
        self._lblJudul = TitleLabel("Catat Aktivitas Karbon")
        setFont(self._lblJudul, 18)
        self._lblJudul.setStyleSheet(_white)

        # Kategori
        self._lblKategori = BodyLabel("Kategori Aktivitas")
        self._lblKategori.setStyleSheet(_white)
        self._cbKategori = ComboBox()
        self._cbKategori.addItems(KATEGORI_LIST)

        # Tanggal
        self._lblTanggal = BodyLabel("Tanggal")
        self._lblTanggal.setStyleSheet(_white)
        self._datePicker = CalendarPicker()
        self._datePicker.setDate(QDate.currentDate())

        # Nilai Aktivitas
        self._lblNilai = BodyLabel("Besaran Aktivitas")
        self._lblNilai.setStyleSheet(_white)
        self._spinNilai = DoubleSpinBox()
        self._spinNilai.setRange(0.01, 999_999.99)
        self._spinNilai.setDecimals(2)
        self._spinNilai.setSingleStep(1.0)

        # Satuan
        self._lblSatuan = BodyLabel("Satuan")
        self._lblSatuan.setStyleSheet(_white)
        self._cbSatuan = ComboBox()
        self._cbSatuan.addItems(list(dict.fromkeys(SATUAN_MAP.values())))

        # Tombol aksi
        self._btnSimpan = PrimaryPushButton(FluentIcon.SAVE, "Simpan")
        self._btnBatal = PushButton(FluentIcon.CLOSE, "Batal")
        self._btnSimpan.setFixedWidth(120)
        self._btnBatal.setFixedWidth(120)

    def _buatLayout(self):
        """Menyusun layout form di dalam dialog."""
        # Form layout
        formLayout = QFormLayout()
        formLayout.setSpacing(14)
        formLayout.setContentsMargins(0, 0, 0, 0)
        formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        formLayout.addRow(self._lblKategori, self._cbKategori)
        formLayout.addRow(self._lblTanggal, self._datePicker)
        formLayout.addRow(self._lblNilai, self._spinNilai)
        formLayout.addRow(self._lblSatuan, self._cbSatuan)

        # Baris tombol
        btnLayout = QHBoxLayout()
        btnLayout.addStretch()
        btnLayout.addWidget(self._btnBatal)
        btnLayout.addWidget(self._btnSimpan)

        # Root layout dialog
        rootLayout = QVBoxLayout(self)
        rootLayout.setContentsMargins(32, 28, 32, 24)
        rootLayout.setSpacing(20)
        rootLayout.addWidget(self._lblJudul)
        rootLayout.addLayout(formLayout)
        rootLayout.addSpacing(8)
        rootLayout.addLayout(btnLayout)

        # Warna teks putih untuk semua label di form
        self.setStyleSheet("""
            TitleLabel, BodyLabel {
                color: white;
            }
        """)

    def _hubungkanSinyal(self):
        """Menghubungkan sinyal widget ke slot."""
        self._btnSimpan.clicked.connect(self.simpanForm)
        self._btnBatal.clicked.connect(self.reject)
        self._cbKategori.currentTextChanged.connect(self._onKategoriChanged)

    def _onKategoriChanged(self, kategori: str):
        satuan = SATUAN_MAP.get(kategori, "")
        idx = self._cbSatuan.findText(satuan)
        if idx >= 0:
            self._cbSatuan.setCurrentIndex(idx)

    def _resetForm(self):
        """Mengosongkan form ke kondisi default."""
        self._logTerpilih = None
        self._cbKategori.setCurrentIndex(0)
        self._datePicker.setDate(QDate.currentDate())
        self._spinNilai.setValue(0.0)
        self._cbSatuan.setCurrentIndex(0)
        self._lblJudul.setText("Catat Aktivitas Karbon")

    # ------------------------------------------------------------------ #
    #  Public methods (sesuai sequence diagram)                           #
    # ------------------------------------------------------------------ #

    def tampilkan(self) -> None:
        """
        Memuat daftar log dari controller lalu membuka dialog.
        (Titik masuk utama sesuai sequence diagram.)
        """
        self._controller.dapatkanDaftarLog()
        self.exec()

    def fillForm(self, logData: LogAktivitas) -> None:
        """
        Mengisi field form dari data LogAktivitas yang dipilih,
        lalu memberitahu controller bahwa log ini sedang diedit.
        Dipanggil sebelum tampilkan() saat mode edit.
        """
        self._logTerpilih = logData
        self._lblJudul.setText("Edit Aktivitas Karbon")

        # Isi widget dari data log
        idx = self._cbKategori.findText(logData.kategori or "")
        self._cbKategori.setCurrentIndex(idx if idx >= 0 else 0)

        if logData.tanggal:
            qd = QDate(logData.tanggal.year, logData.tanggal.month, logData.tanggal.day)
            self._datePicker.setDate(qd)

        self._spinNilai.setValue(logData.nilaiAktivitas or 0.0)

        idx_satuan = self._cbSatuan.findText(logData.satuanAktivitas or "")
        self._cbSatuan.setCurrentIndex(idx_satuan if idx_satuan >= 0 else 0)

        # Beritahu controller bahwa log ini sedang diedit
        ok = self._controller.ubahLog(logData)
        if not ok:
            self.tampilkanError("Data log tidak valid untuk diedit.")

    def simpanForm(self) -> None:
        """
        Mengumpulkan input dari form, lalu memanggil controller.simpanLog().
        Menampilkan notifikasi sukses atau error.
        """
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
        """Menampilkan notifikasi error menggunakan QFluentWidgets InfoBar."""
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
        """Menampilkan notifikasi sukses menggunakan QFluentWidgets InfoBar."""
        InfoBar.success(
            title="Berhasil Disimpan",
            content="Log aktivitas karbon berhasil dicatat.",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=3000,
            position=InfoBarPosition.TOP,
            parent=self.parent(),
        )
