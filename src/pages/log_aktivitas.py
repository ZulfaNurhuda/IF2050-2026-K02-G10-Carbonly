from typing import List, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QLabel,
)
from qfluentwidgets import (
    TitleLabel,
    BodyLabel,
    PrimaryPushButton,
    PushButton,
    InfoBar,
    InfoBarPosition,
    TableWidget,
    FluentIcon,
    setFont,
    isDarkTheme,
    MessageBox,
)

from src.controllers.LogAktivitasController import LogAktivitasController
from src.models.LogAktivitas import LogAktivitas
from src.views.FormLogAktivitasView import FormLogAktivitasView


class LogAktivitasPage(QWidget):
    """
    Halaman utama Log Aktivitas Karbon.

    Menampilkan daftar log dalam tabel dan menyediakan tombol
    'Tambah Log' di pojok kanan atas yang membuka FormLogAktivitasView
    sebagai dialog modal.
    """

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("log-aktivitas-page")

        self._controller = LogAktivitasController()

        self._buatWidget()
        self._buatLayout()
        self._hubungkanSinyal()
        self._muatDaftarLog()

    # ------------------------------------------------------------------ #
    #  Widget & Layout                                                     #
    # ------------------------------------------------------------------ #

    def _buatWidget(self):
        """Membuat semua widget halaman."""
        # Header — judul
        self._lblJudul = TitleLabel("Log Aktivitas Karbon")
        setFont(self._lblJudul, 22)

        self._lblSubjudul = BodyLabel("Catat dan kelola aktivitas karbon harian Anda.")

        # Tombol kanan atas
        self._btnTambah = PrimaryPushButton(FluentIcon.ADD, "Tambah Log")
        self._btnTambah.setFixedHeight(36)

        # Tabel daftar log
        self._tabel = TableWidget(self)
        self._tabel.setColumnCount(6)
        self._tabel.setHorizontalHeaderLabels(
            ["ID", "Tanggal", "Kategori", "Besaran", "Satuan", "Total Emisi (kg CO2e)"]
        )
        self._tabel.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._tabel.hideColumn(0) 
        self._tabel.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._tabel.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._tabel.setAlternatingRowColors(True)
        self._tabel.verticalHeader().setVisible(False)

        # Tombol aksi baris (edit & hapus)
        self._btnEdit = PushButton(FluentIcon.EDIT, "Edit")
        self._btnHapus = PushButton(FluentIcon.DELETE, "Hapus")
        self._btnEdit.setEnabled(False)
        self._btnHapus.setEnabled(False)
        self._btnEdit.setFixedHeight(34)
        self._btnHapus.setFixedHeight(34)

    def _buatLayout(self):
        """Menyusun layout halaman."""
        # Baris header: judul kiri, tombol tambah kanan
        headerLayout = QHBoxLayout()
        headerLayout.setContentsMargins(0, 0, 0, 0)

        judulCol = QVBoxLayout()
        judulCol.setSpacing(2)
        judulCol.addWidget(self._lblJudul)
        judulCol.addWidget(self._lblSubjudul)

        headerLayout.addLayout(judulCol)
        headerLayout.addStretch()
        headerLayout.addWidget(self._btnTambah, alignment=Qt.AlignmentFlag.AlignTop)

        # Baris tombol aksi baris tabel
        aksiLayout = QHBoxLayout()
        aksiLayout.addWidget(self._btnEdit)
        aksiLayout.addWidget(self._btnHapus)
        aksiLayout.addStretch()

        # Root layout
        rootLayout = QVBoxLayout(self)
        rootLayout.setContentsMargins(36, 28, 36, 28)
        rootLayout.setSpacing(16)
        rootLayout.addLayout(headerLayout)
        rootLayout.addLayout(aksiLayout)
        rootLayout.addWidget(self._tabel)

    def _hubungkanSinyal(self):
        """Menghubungkan sinyal ke slot."""
        self._btnTambah.clicked.connect(self._bukaFormTambah)
        self._btnEdit.clicked.connect(self._bukaFormEdit)
        self._btnHapus.clicked.connect(self._konfirmasiHapus)
        self._tabel.itemSelectionChanged.connect(self._onSeleksiTabelBerubah)

    # ------------------------------------------------------------------ #
    #  Slot                                                                #
    # ------------------------------------------------------------------ #

    def _onSeleksiTabelBerubah(self):
        """Aktifkan/nonaktifkan tombol Edit & Hapus berdasarkan seleksi."""
        dipilih = len(self._tabel.selectedItems()) > 0
        self._btnEdit.setEnabled(dipilih)
        self._btnHapus.setEnabled(dipilih)

    def _bukaFormTambah(self) -> None:
        """Membuka FormLogAktivitasView sebagai dialog tambah baru."""
        dialog = FormLogAktivitasView(controller=self._controller, parent=self)
        dialog.logDisimpan.connect(self._muatDaftarLog)
        dialog.exec()

    def _bukaFormEdit(self) -> None:
        """Membuka FormLogAktivitasView sebagai dialog edit untuk baris terpilih."""
        log = self._logDariBarisTerpilih()
        if log is None:
            return

        dialog = FormLogAktivitasView(
            controller=self._controller,
            logTerpilih=log,
            parent=self,
        )
        dialog.fillForm(log)
        dialog.logDisimpan.connect(self._muatDaftarLog)
        dialog.exec()

    def _konfirmasiHapus(self) -> None:
        """Menampilkan konfirmasi sebelum menghapus log."""
        log = self._logDariBarisTerpilih()
        if log is None:
            return

        dlg = MessageBox(
            "Hapus Log",
            f"Yakin ingin menghapus log '{log.kategori}' "
            f"pada {log.tanggal.strftime('%d %b %Y')}?",
            self,
        )
        if dlg.exec():
            self._controller.hapusLog(log.id)
            self._muatDaftarLog()
            InfoBar.success(
                title="Dihapus",
                content="Log aktivitas berhasil dihapus.",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                duration=3000,
                position=InfoBarPosition.TOP,
                parent=self,
            )

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _logDariBarisTerpilih(self) -> Optional[LogAktivitas]:
        """Mengambil objek LogAktivitas dari baris yang sedang dipilih di tabel."""
        baris = self._tabel.currentRow()
        if baris < 0:
            return None
        id_item = self._tabel.item(baris, 0)
        if id_item is None:
            return None
        return id_item.data(Qt.ItemDataRole.UserRole)

    def _muatDaftarLog(self) -> None:
        """Mengambil daftar log dari controller dan memperbarui tabel."""
        daftar: List[LogAktivitas] = self._controller.dapatkanDaftarLog()

        self._tabel.setRowCount(0)
        for log in daftar:
            baris = self._tabel.rowCount()
            self._tabel.insertRow(baris)

            # Kolom ID — simpan objek log di UserRole agar bisa diambil kembali
            id_item = QTableWidgetItem(str(log.id))
            id_item.setData(Qt.ItemDataRole.UserRole, log)
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            tanggal_str = log.tanggal.strftime("%d %b %Y") if log.tanggal else "-"
            emisi_str = f"{log.totalEmisi:.2f}" if log.totalEmisi is not None else "-"

            items = [
                id_item,
                QTableWidgetItem(tanggal_str),
                QTableWidgetItem(log.kategori or "-"),
                QTableWidgetItem(str(log.nilaiAktivitas or "-")),
                QTableWidgetItem(log.satuanAktivitas or "-"),
                QTableWidgetItem(emisi_str),
            ]

            for col, item in enumerate(items):
                if col > 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self._tabel.setItem(baris, col, item)

        # Reset seleksi & tombol aksi
        self._btnEdit.setEnabled(False)
        self._btnHapus.setEnabled(False)
