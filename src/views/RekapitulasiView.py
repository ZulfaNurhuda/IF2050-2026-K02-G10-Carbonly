# ruff: noqa
# flake8: noqa
# mypy: ignore-errors
from datetime import datetime, time, timedelta
from typing import Optional, TYPE_CHECKING

from src.controllers.RekapitulasiController import RekapitulasiController

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from qfluentwidgets import (
    SegmentedWidget,
    TransparentToolButton,
    SubtitleLabel,
    CardWidget,
    BodyLabel,
    TitleLabel,
    FluentIcon,
)

from PyQt6.QtCharts import (
    QChart,
    QChartView,
    QBarSet,
    QBarSeries,
    QBarCategoryAxis,
    QValueAxis,
)


class RekapitulasiView(QWidget):
    def __init__(
        self,
        parent=None,
        controller: Optional[RekapitulasiController] = None,
        tanggalMulai: Optional[datetime] = None,
        tanggalAkhir: Optional[datetime] = None,
    ):
        super().__init__(parent=parent)
        self._controller = controller if controller is not None else RekapitulasiController()
        self.current_date = datetime.now() if tanggalMulai is None else tanggalMulai
        self.current_mode = "Harian"
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
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(12)

        self.pivot = SegmentedWidget(self)
        self.pivot.addItem("Harian", "Harian")
        self.pivot.addItem("Mingguan", "Mingguan")
        self.pivot.currentItemChanged.connect(self.onModeChanged)
        self.main_layout.addWidget(self.pivot, 0, Qt.AlignmentFlag.AlignLeft)

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
        self.main_layout.addLayout(self.cards_layout)

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setMinimumHeight(280)
        self.main_layout.addWidget(self.chart_view, 1)

        self.pivot.setCurrentItem("Harian")

    def onModeChanged(self, mode: str):
        self.current_mode = mode
        if mode == "Mingguan":
            self.current_date = self.current_date - timedelta(
                days=self.current_date.weekday()
            )
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

    def _weekRange(self):
        d = self.current_date.date()
        start = datetime.combine(d - timedelta(days=d.weekday()), time.min)
        end = datetime.combine(d + timedelta(days=6 - d.weekday()), time.max)
        return start, end

    @staticmethod
    def _startOfDay(dt: datetime) -> datetime:
        return datetime.combine(dt.date(), time.min)

    @staticmethod
    def _endOfDay(dt: datetime) -> datetime:
        return datetime.combine(dt.date(), time.max)

    def _updateDateLabel(self):
        if self.current_mode == "Harian":
            self.date_label.setText(self.current_date.strftime("%d %B %Y"))
            return

        week_start, week_end = self._weekRange()
        today = datetime.now()
        today_week_start = today - timedelta(days=today.weekday())
        delta_days = (week_start - today_week_start).days
        delta_weeks = delta_days // 7

        if delta_weeks == 0:
            label_text = "Minggu ini"
        elif delta_weeks == 1:
            label_text = "Minggu Depan"
        elif delta_weeks == -1:
            label_text = "Minggu Lalu"
        else:
            label_text = (
                f"{week_start.strftime('%d %b %Y')} - {week_end.strftime('%d %b %Y')}"
            )
        self.date_label.setText(label_text)

    def _updateCardLabels(self):
        if self.current_mode == "Harian":
            self.lbl_card_emisi_title.setText("Emisi Hari Ini")
            self.lbl_card_target_title.setText("Target Harian")
        else:
            self.lbl_card_emisi_title.setText("Emisi Minggu ini")
            self.lbl_card_target_title.setText("Target Minggu Ini")

    def _updateChart(self):
        self.chart.setTitle(
            "Grafik Emisi Harian" if self.current_mode == "Harian" else "Grafik Emisi Mingguan"
        )
        self.chart.removeAllSeries()
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        series = QBarSeries()
        bar_set = QBarSet("Emisi")
        categories = []
        max_val = 0

        if self.current_mode == "Harian":
            week_start, week_end = self._weekRange()
            values_by_date = {}
            if self._controller is not None:
                data = self._controller.dapatkanRekapitulasi(week_start, week_end)
                for d, val in data.get("emisi_per_hari", []):
                    values_by_date[d.date()] = val
            for i in range(7):
                day = week_start + timedelta(days=i)
                val = values_by_date.get(day.date(), 0.0)
                bar_set.append(val)
                categories.append(day.strftime("%a"))
                if val > max_val:
                    max_val = val
        else:
            d = self.current_date.date()
            current_week_start = datetime.combine(d - timedelta(days=d.weekday()), time.min)
            num_weeks = 8
            first_week_start = current_week_start - timedelta(weeks=num_weeks - 1)
            overall_end = datetime.combine(d + timedelta(days=6 - d.weekday()), time.max)
            values_by_week = {}
            if self._controller is not None:
                data = self._controller.dapatkanRekapitulasi(first_week_start, overall_end)
                for d_item, val in data.get("emisi_per_hari", []):
                    wk_start = d_item - timedelta(days=d_item.weekday())
                    values_by_week[wk_start.date()] = values_by_week.get(wk_start.date(), 0.0) + val
            for i in range(num_weeks):
                wk_start = first_week_start + timedelta(weeks=i)
                val = values_by_week.get(wk_start.date(), 0.0)
                bar_set.append(val)
                categories.append(wk_start.strftime("%d %b"))
                if val > max_val:
                    max_val = val

        series.append(bar_set)
        self.chart.addSeries(series)

        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsAngle(-30)
        axisX.setLabelsFont(QFont("Segoe UI", 9))
        self.chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText("kg CO2e")
        axisY.setRange(0, max_val * 1.2 if max_val > 0 else 10)
        axisY.setLabelsFont(QFont("Segoe UI", 9))
        self.chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)

    def loadData(self):
        self._updateDateLabel()
        self._updateCardLabels()
        self._updateChart()

        total_emisi = 0.0
        target_emisi = 0.0
        week_start, week_end = self._weekRange()

        if self._controller is not None:
            if self.current_mode == "Harian":
                data = self._controller.dapatkanRekapitulasi(
                    self._startOfDay(self.current_date),
                    self._endOfDay(self.current_date),
                )
            else:
                data = self._controller.dapatkanRekapitulasi(week_start, week_end)

            total_emisi = data.get("total_emisi", 0.0)
            target_emisi = data.get("target_emisi", 0.0)

        self.lbl_card_emisi_value.setText(f"{total_emisi:.2f} kg CO2e")
        self.lbl_card_target_value.setText(f"{target_emisi:.2f} kg CO2e")

        if target_emisi > 0 and total_emisi > target_emisi:
            self.lbl_card_emisi_value.setStyleSheet("color: red;")
        else:
            self.lbl_card_emisi_value.setStyleSheet("color: green;")

    def refresh(self):
        self.loadData()
