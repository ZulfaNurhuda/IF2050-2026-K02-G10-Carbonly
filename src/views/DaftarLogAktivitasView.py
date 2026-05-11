from typing import List, Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QHeaderView, QTableWidgetItem
from PyQt6.QtCore import Qt
from qfluentwidgets import TableWidget, SubtitleLabel, PushButton, MessageBox, InfoBar, InfoBarPosition

class DaftarLogAktivitasView(QWidget):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        controller: Optional["LogAktivitasController"] = None,
        logTerpilih: Optional["LogAktivitas"] = None,
        daftarLog: Optional[List["LogAktivitas"]] = None,
    ):
        super().__init__(parent=parent)
        self.setObjectName("DaftarLogAktivitasView")
        
        self._controller = controller
        self._logTerpilih = logTerpilih
        self._daftarLog = daftarLog if daftarLog is not None else []

        # Setup User Interface
        self.setupUI()

    def setupUI(self):
        # Layout Utama
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)

        # Judul Halaman
        self.titleLabel = SubtitleLabel("Daftar Log Aktivitas", self)
        self.layout.addWidget(self.titleLabel)

        # Tabel Log Aktivitas (qfluentwidgets TableWidget)
        self.table = TableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'Tanggal', 'Kategori', 'Besaran', 'Emisi (kg CO2e)', 'Komentar'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(TableWidget.EditTrigger.NoEditTriggers) # Read-only table
        self.table.setSelectionBehavior(TableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(TableWidget.SelectionMode.SingleSelection)
        self.layout.addWidget(self.table)

        # Tombol Aksi (Ubah dan Hapus)
        self.btnLayout = QHBoxLayout()
        self.btnUbah = PushButton("Ubah Log", self)
        self.btnHapus = PushButton("Hapus Log", self)
        
        self.btnLayout.addStretch(1)
        self.btnLayout.addWidget(self.btnUbah)
        self.btnLayout.addWidget(self.btnHapus)
        self.layout.addLayout(self.btnLayout)

        # Event Listeners
        self.table.itemSelectionChanged.connect(self._onSelectionChanged)
        self.btnHapus.clicked.connect(self.konfirmasi)
        
        # Note: btnUbah.clicked.connect(self.ubahLog) bisa dihubungkan nanti untuk UC04

    # === PROPERTIES ===
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
        self.tunjukkanDaftarLog(self._daftarLog)

    # === METHODS ===
    def tampilkan(self) -> None:
        """Dipanggil untuk me-refresh/mengambil data terbaru dari controller (UC02)"""
        if self._controller:
            logs = self._controller.dapatkanDaftarLog()
            if logs and len(logs) > 0:
                self.tunjukkanDaftarLog(logs)
            else:
                self.tunjukkanKosong()

    def _onSelectionChanged(self):
        """Menangkap event ketika pengguna mengklik baris di tabel"""
        selected_rows = self.table.selectedItems()
        if selected_rows and len(self._daftarLog) > 0:
            row_index = selected_rows[0].row()
            self.pilihLog(self._daftarLog[row_index])

    def pilihLog(self, log: "LogAktivitas") -> None:
        self.logTerpilih = log

    def konfirmasi(self) -> None:
        """Menampilkan dialog konfirmasi penghapusan (Skenario UC05)"""
        if not self.logTerpilih:
            InfoBar.warning(
                title="Peringatan",
                content="Pilih log yang ingin dihapus terlebih dahulu.",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return

        dialog = MessageBox(
            "Konfirmasi Hapus",
            "Yakin ingin menghapus log yang dipilih?\nTindakan ini tidak dapat dibatalkan.",
            self
        )
        
        # Jika pengguna menekan tombol "Yes" / konfirmasi
        if dialog.exec():
            self.hapusLog()
        else:
            self.batal()

    def hapusLog(self) -> None:
        """Mengeksekusi penghapusan log ke controller (UC05)"""
        if self._controller and self.logTerpilih:
            # Asumsi model LogAktivitas memiliki atribut 'id'
            self._controller.hapusLog(self.logTerpilih.id) 
            self.logTerpilih = None
            
            # Tampilkan pesan sukses
            InfoBar.success(
                title="Sukses",
                content="Log berhasil dihapus secara permanen.",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            # Refresh tabel
            self.tampilkan()

    def batal(self) -> None:
        """Aksi ketika penghapusan dibatalkan"""
        self.tutupKonfirmasi()

    def tutupKonfirmasi(self) -> None:
        pass # MessageBox otomatis tertutup, bisa digunakan untuk custom flag jika perlu

    def tunjukkanDaftarLog(self, daftarLog: List["LogAktivitas"]) -> None:
        """Merender data array LogAktivitas ke dalam qfluentwidgets TableWidget"""
        self._daftarLog = daftarLog
        self.table.setRowCount(len(daftarLog))
        
        for row, log in enumerate(daftarLog):
            # Asumsi model LogAktivitas memiliki atribut berikut:
            # tanggal, kategori, besaran, nilai_emisi, komentar
            # Silakan sesuaikan nama atribut dengan Class Model C02 Anda
            
            self.table.setItem(row, 0, QTableWidgetItem(str(getattr(log, 'tanggal', ''))))
            self.table.setItem(row, 1, QTableWidgetItem(str(getattr(log, 'kategori', ''))))
            self.table.setItem(row, 2, QTableWidgetItem(str(getattr(log, 'besaran', ''))))
            self.table.setItem(row, 3, QTableWidgetItem(f"{getattr(log, 'nilai_emisi', 0):.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(str(getattr(log, 'komentar', ''))))

    def tunjukkanKosong(self) -> None:
        """Tampilan jika belum ada log aktivitas"""
        self._daftarLog = []
        self.table.setRowCount(0)
        # Menampilkan tabel kosong, pesan opsional
        InfoBar.info(
            title="Informasi",
            content="Belum ada log aktivitas yang tercatat.",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=3000,
            parent=self
        )