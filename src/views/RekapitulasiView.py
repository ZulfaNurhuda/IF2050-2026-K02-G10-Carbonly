from datetime import datetime, timedelta
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.controllers.RekapitulasiController import RekapitulasiController

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QStackedWidget, QTableWidgetItem, QHeaderView)

from qfluentwidgets import (SegmentedWidget, TransparentToolButton, SubtitleLabel, 
                            CardWidget, TableWidget, BodyLabel, TitleLabel, FluentIcon)

from PyQt6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis

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
        
        # Default view is Harian for today
        self.current_date = datetime.now() if tanggalMulai is None else tanggalMulai
        self.current_mode = "Harian" # "Harian" or "Mingguan"
        
        self.initUI()
        self.loadData()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value):
        self._controller = value
        self.loadData()

    def initUI(self):
        self.setObjectName("RekapitulasiView")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(16)

        # Title
        self.title_label = TitleLabel("Rekapitulasi Emisi", self)
        self.main_layout.addWidget(self.title_label)

        # Toggle Harian/Mingguan
        self.pivot = SegmentedWidget(self)
        self.pivot.addItem("Harian", "Harian", self.onModeChanged)
        self.pivot.addItem("Mingguan", "Mingguan", self.onModeChanged)
        self.main_layout.addWidget(self.pivot, 0, Qt.AlignmentFlag.AlignLeft)

        # Navigation Row
        self.nav_layout = QHBoxLayout()
        self.btn_prev = TransparentToolButton(FluentIcon.LEFT_ARROW, self)
        self.btn_prev.clicked.connect(self.prevDate)
        
        self.date_label = SubtitleLabel("Tanggal", self)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_next = TransparentToolButton(FluentIcon.RIGHT_ARROW, self)
        self.btn_next.clicked.connect(self.nextDate)
        
        self.nav_layout.addWidget(self.btn_prev)
        self.nav_layout.addWidget(self.date_label, 1)
        self.nav_layout.addWidget(self.btn_next)
        self.main_layout.addLayout(self.nav_layout)

        # Stacked Widget for Harian vs Mingguan content
        self.stacked_widget = QStackedWidget(self)
        self.main_layout.addWidget(self.stacked_widget, 1)

        # ---- HARIAN VIEW ----
        self.harian_widget = QWidget()
        self.harian_layout = QVBoxLayout(self.harian_widget)
        self.harian_layout.setContentsMargins(0, 0, 0, 0)
        self.harian_layout.setSpacing(16)
        
        # Cards
        self.cards_layout = QHBoxLayout()
        self.card_emisi = CardWidget(self)
        self.card_emisi_layout = QVBoxLayout(self.card_emisi)
        self.lbl_card_emisi_title = BodyLabel("Emisi Hari Ini", self)
        self.lbl_card_emisi_value = TitleLabel("0 kg CO2e", self)
        self.card_emisi_layout.addWidget(self.lbl_card_emisi_title)
        self.card_emisi_layout.addWidget(self.lbl_card_emisi_value)
        
        self.card_target = CardWidget(self)
        self.card_target_layout = QVBoxLayout(self.card_target)
        self.lbl_card_target_title = BodyLabel("Target Harian", self)
        self.lbl_card_target_value = TitleLabel("0 kg CO2e", self)
        self.card_target_layout.addWidget(self.lbl_card_target_title)
        self.card_target_layout.addWidget(self.lbl_card_target_value)
        
        self.cards_layout.addWidget(self.card_emisi)
        self.cards_layout.addWidget(self.card_target)
        self.harian_layout.addLayout(self.cards_layout)

        # Table
        self.lbl_tabel = SubtitleLabel("Log Aktivitas", self)
        self.harian_layout.addWidget(self.lbl_tabel)
        
        self.table_widget = TableWidget(self)
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Kategori", "Aktivitas", "Besaran", "Emisi", "Komentar"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.harian_layout.addWidget(self.table_widget, 1)
        
        self.stacked_widget.addWidget(self.harian_widget)

        # ---- MINGGUAN VIEW ----
        self.mingguan_widget = QWidget()
        self.mingguan_layout = QVBoxLayout(self.mingguan_widget)
        self.mingguan_layout.setContentsMargins(0, 0, 0, 0)
        
        self.chart = QChart()
        self.chart.setTitle("Grafik Emisi Mingguan")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self.mingguan_layout.addWidget(self.chart_view, 1)
        self.stacked_widget.addWidget(self.mingguan_widget)
        
        # Set default
        self.pivot.setCurrentItem("Harian")

    def onModeChanged(self, mode: str):
        self.current_mode = mode
        if mode == "Harian":
            self.stacked_widget.setCurrentWidget(self.harian_widget)
        else:
            # Set to beginning of the week (Monday)
            self.current_date = self.current_date - timedelta(days=self.current_date.weekday())
            self.stacked_widget.setCurrentWidget(self.mingguan_widget)
        self.loadData()

    def prevDate(self):
        if self.current_mode == "Harian":
            self.current_date -= timedelta(days=1)
        else:
            self.current_date -= timedelta(days=7)
        self.loadData()

    def nextDate(self):
        if self.current_mode == "Harian":
            self.current_date += timedelta(days=1)
        else:
            self.current_date += timedelta(days=7)
        self.loadData()

    def loadData(self):
        if not self._controller:
            return
            
        if self.current_mode == "Harian":
            self.date_label.setText(self.current_date.strftime("%d %B %Y"))
            # Panggil method sesuai class diagram DPPL
            data = self._controller.dapatkanRekapitulasi(self.current_date, self.current_date)
            
            total_emisi = data.get("total_emisi", 0.0)
            target_emisi = data.get("target_emisi", 0.0)
            logs = data.get("log", [])
            
            self.lbl_card_emisi_value.setText(f"{total_emisi:.2f} kg CO2e")
            self.lbl_card_target_value.setText(f"{target_emisi:.2f} kg CO2e")
            
            # Badge logic
            if target_emisi > 0 and total_emisi > target_emisi:
                self.lbl_card_emisi_value.setStyleSheet("color: red;")
            else:
                self.lbl_card_emisi_value.setStyleSheet("color: green;")
                
            # Populate Table
            self.table_widget.setRowCount(len(logs))
            for i, log in enumerate(logs):
                kategori = getattr(log, 'kategori', "-")
                aktivitas = getattr(log, 'namaAktivitas', "-")
                besaran = f"{getattr(log, 'nilaiAktivitas', 0)} {getattr(log, 'satuanAktivitas', '')}"
                emisi = str(getattr(log, 'totalEmisi', 0.0))
                komentar = getattr(log, 'komentar', "-")
                
                self.table_widget.setItem(i, 0, QTableWidgetItem(str(kategori)))
                self.table_widget.setItem(i, 1, QTableWidgetItem(str(aktivitas)))
                self.table_widget.setItem(i, 2, QTableWidgetItem(str(besaran)))
                self.table_widget.setItem(i, 3, QTableWidgetItem(str(emisi)))
                self.table_widget.setItem(i, 4, QTableWidgetItem(str(komentar)))
                
        else:
            # Mingguan
            start_date = self.current_date
            end_date = start_date + timedelta(days=6)
            self.date_label.setText(f"{start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}")
            
            # Panggil method sesuai class diagram DPPL
            data = self._controller.dapatkanRekapitulasi(start_date, end_date)
            emisi_per_hari = data.get("emisi_per_hari", [])
            
            # Update Chart
            self.chart.removeAllSeries()
            for axis in self.chart.axes():
                self.chart.removeAxis(axis)
                
            series = QBarSeries()
            bar_set = QBarSet("Emisi Harian")
            categories = []
            
            max_val = 0
            for d, val in emisi_per_hari:
                bar_set.append(val)
                categories.append(d.strftime("%a"))
                if val > max_val: max_val = val
                
            series.append(bar_set)
            self.chart.addSeries(series)
            
            axisX = QBarCategoryAxis()
            axisX.append(categories)
            self.chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
            series.attachAxis(axisX)
            
            axisY = QValueAxis()
            axisY.setTitleText("kg CO2e")
            axisY.setRange(0, max_val * 1.2 if max_val > 0 else 10)
            self.chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
            series.attachAxis(axisY)
