from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.controllers.RekapitulasiController import RekapitulasiController

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import CalendarPicker, PrimaryPushButton, SubtitleLabel, ProgressRing, CardWidget, setFont

class RekapitulasiView(QWidget):
    def __init__(
        self,
        parent=None,
        controller: Optional["RekapitulasiController"] = None,
        tanggalMulai: Optional[datetime] = None,
        tanggalAkhir: Optional[datetime] = None,
    ):
        super().__init__(parent=parent)
        self._controller = controller
        self._tanggalMulai = tanggalMulai
        self._tanggalAkhir = tanggalAkhir
        
        self.initUI()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value):
        self._controller = value

    @property
    def tanggalMulai(self):
        return self._tanggalMulai

    @tanggalMulai.setter
    def tanggalMulai(self, value):
        self._tanggalMulai = value

    @property
    def tanggalAkhir(self):
        return self._tanggalAkhir

    @tanggalAkhir.setter
    def tanggalAkhir(self, value):
        self._tanggalAkhir = value

    def initUI(self):
        self.setObjectName("RekapitulasiView")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(16)

        self.title_label = SubtitleLabel("Rekapitulasi Emisi", self)
        setFont(self.title_label, 20)
        self.main_layout.addWidget(self.title_label)

        self.date_layout = QHBoxLayout()
        self.date_layout.setSpacing(16)

        self.start_date_picker = CalendarPicker(self)
        self.end_date_picker = CalendarPicker(self)
        
        self.date_layout.addWidget(QLabel("Tanggal Mulai:", self))
        self.date_layout.addWidget(self.start_date_picker)
        self.date_layout.addWidget(QLabel("Tanggal Akhir:", self))
        self.date_layout.addWidget(self.end_date_picker)
        
        self.main_layout.addLayout(self.date_layout)

        self.tampilkan_btn = PrimaryPushButton("Tampilkan", self)
        self.tampilkan_btn.clicked.connect(self.tampilkan)
        self.main_layout.addWidget(self.tampilkan_btn)

        self.result_card = CardWidget(self)
        self.result_layout = QVBoxLayout(self.result_card)
        self.result_layout.setSpacing(16)
        
        self.total_emisi_label = SubtitleLabel("Total Emisi: -", self.result_card)
        self.target_emisi_label = SubtitleLabel("Target Emisi: -", self.result_card)
        
        self.progress_ring = ProgressRing(self.result_card)
        self.progress_ring.setFixedSize(120, 120)
        self.progress_ring.setTextVisible(True)
        self.progress_ring.setValue(0)
        
        self.progress_layout = QHBoxLayout()
        self.progress_layout.addWidget(self.progress_ring, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.result_layout.addWidget(self.total_emisi_label)
        self.result_layout.addWidget(self.target_emisi_label)
        self.result_layout.addLayout(self.progress_layout)

        self.empty_label = SubtitleLabel("Data tidak tersedia.", self.result_card)
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.hide()
        self.result_layout.addWidget(self.empty_label)

        self.main_layout.addWidget(self.result_card)
        self.main_layout.addStretch(1)

    def tampilkan(self) -> None:
        qdate_start = self.start_date_picker.getDate()
        qdate_end = self.end_date_picker.getDate()
        
        if not qdate_start.isValid() or not qdate_end.isValid():
            self.tunjukkanKosong()
            return
            
        start_datetime = datetime(qdate_start.year(), qdate_start.month(), qdate_start.day())
        end_datetime = datetime(qdate_end.year(), qdate_end.month(), qdate_end.day())
        
        self.pilihRentang(start_datetime, end_datetime)

    def pilihRentang(self, tanggalMulai: datetime, tanggalAkhir: datetime) -> None:
        self.tanggalMulai = tanggalMulai
        self.tanggalAkhir = tanggalAkhir
        if self._controller:
            data = self._controller.dapatkanRekapitulasi(tanggalMulai, tanggalAkhir)
            self.tunjukkanRekapitulasi(data)
        else:
            self.tunjukkanKosong()

    def tunjukkanRekapitulasi(self, data: object) -> None:
        if not data or not isinstance(data, dict):
            self.tunjukkanKosong()
            return
            
        total_emisi = data.get("total_emisi", 0.0)
        target_emisi = data.get("target_emisi", 0.0)
        
        if target_emisi > 0:
            percentage = (total_emisi / target_emisi) * 100
        else:
            percentage = 0.0
            
        self.total_emisi_label.setText(f"Total Emisi: {total_emisi:.2f}")
        self.target_emisi_label.setText(f"Target Emisi: {target_emisi:.2f}")
        self.progress_ring.setValue(min(int(percentage), 100))
        self.progress_ring.setFormat(f"{percentage:.1f}%")
        
        self.total_emisi_label.show()
        self.target_emisi_label.show()
        self.progress_ring.show()
        self.empty_label.hide()

    def tunjukkanKosong(self) -> None:
        self.total_emisi_label.hide()
        self.target_emisi_label.hide()
        self.progress_ring.hide()
        self.empty_label.show()
