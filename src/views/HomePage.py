from datetime import datetime, time, timedelta
from typing import Dict, List, Optional, Tuple

from PyQt6.QtCharts import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QChartView,
    QValueAxis,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPainter
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QScrollArea,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    FluentIcon,
    InfoBar,
    InfoBarPosition,
    MessageBox,
    PrimaryPushButton,
    PushButton,
    SegmentedWidget,
    SubtitleLabel,
    TableWidget,
    TitleLabel,
    TransparentToolButton,
    setFont,
    themeColor,
)

from src.controllers.ActivityLogController import ActivityLogController
from src.controllers.AuthController import AuthController
from src.controllers.SummaryController import SummaryController
from src.models.ActivityLog import ActivityLog
from src.views.ActivityLogFormView import ActivityLogFormView
from src.views.EmissionTargetFormView import EmissionTargetFormView


class HomePage(QWidget):
    profile_requested = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("home-page")
        self._header: Optional[HomePage._AppHeader] = None
        self._summary: Optional[HomePage._EmissionSummarySection] = None
        self._activity_log: Optional[HomePage._ActivityLogSection] = None
        self._setup_ui()

    def refresh(self) -> None:
        username = AuthController.get_current_username() or "Pengguna"
        if self._header is not None:
            self._header.set_username(username)
        if self._summary is not None:
            self._summary.refresh()
        if self._activity_log is not None:
            self._activity_log.refresh()

    def _setup_ui(self) -> None:
        username = AuthController.get_current_username() or "Pengguna"

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(16)

        self._header = HomePage._AppHeader(self)
        self._header.profile_clicked.connect(self.profile_requested)
        outer.addWidget(self._header)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent;")
        viewport = scroll.viewport()
        if viewport:
            viewport.setAutoFillBackground(False)

        content = QWidget()
        content.setAutoFillBackground(False)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(4, 8, 4, 8)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        welcome = SubtitleLabel(f"Selamat datang, {username}!", content)
        desc = BodyLabel("Pantau jejak karbon harian kamu di sini.", content)
        desc.setStyleSheet("color: gray;")
        layout.addWidget(welcome)
        layout.addWidget(desc)

        self._summary = HomePage._EmissionSummarySection(content)
        layout.addWidget(self._summary)

        self._activity_log = HomePage._ActivityLogSection(content)
        self._activity_log.data_changed.connect(self._summary.refresh)
        layout.addWidget(self._activity_log)

        layout.addStretch(1)
        scroll.setWidget(content)
        outer.addWidget(scroll)

    class _AppHeader(CardWidget):
        profile_clicked = pyqtSignal()

        def __init__(self, parent: Optional[QWidget] = None) -> None:
            super().__init__(parent)
            self.setFixedHeight(80)

            outer = QHBoxLayout(self)
            outer.setContentsMargins(20, 12, 16, 12)
            outer.setSpacing(12)

            branding_col = QVBoxLayout()
            branding_col.setSpacing(2)

            title = SubtitleLabel("Carbonly", self)
            setFont(title, 26, QFont.Weight.Bold)
            title.setStyleSheet(f"color: {themeColor().name()};")

            from qfluentwidgets import CaptionLabel
            tagline = CaptionLabel("Personal Carbon Footprint Tracker", self)
            tagline.setStyleSheet("color: gray;")

            branding_col.addWidget(title)
            branding_col.addWidget(tagline)

            username = AuthController.get_current_username()
            self._profile_btn = PrimaryPushButton(FluentIcon.PEOPLE, username, self)
            self._profile_btn.clicked.connect(self.profile_clicked)

            outer.addLayout(branding_col)
            outer.addStretch(1)
            outer.addWidget(self._profile_btn)

        def set_username(self, username: str) -> None:
            self._profile_btn.setText(username)

    class _EmissionSummarySection(QWidget):
        def __init__(self, parent: Optional[QWidget] = None) -> None:
            super().__init__(parent)
            self._current_date = datetime.now()
            self._current_mode = "Harian"
            self._setup_ui()
            self._load_data()

        def refresh(self) -> None:
            self._load_data()

        def _setup_ui(self) -> None:
            self._main_layout = QVBoxLayout(self)
            self._main_layout.setContentsMargins(0, 0, 0, 0)
            self._main_layout.setSpacing(12)

            self._pivot = SegmentedWidget(self)
            self._pivot.addItem("Harian", "Harian")
            self._pivot.addItem("Mingguan", "Mingguan")
            self._pivot.currentItemChanged.connect(self._on_mode_changed)
            self._main_layout.addWidget(self._pivot, 0, Qt.AlignmentFlag.AlignLeft)

            nav_layout = QHBoxLayout()
            self._btn_prev = TransparentToolButton(FluentIcon.LEFT_ARROW, self)
            self._btn_prev.clicked.connect(self._on_prev_clicked)

            self._date_label = SubtitleLabel("Tanggal", self)
            self._date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self._btn_next = TransparentToolButton(FluentIcon.RIGHT_ARROW, self)
            self._btn_next.clicked.connect(self._on_next_clicked)

            nav_layout.addWidget(self._btn_prev)
            nav_layout.addWidget(self._date_label, 1)
            nav_layout.addWidget(self._btn_next)
            self._main_layout.addLayout(nav_layout)

            cards_layout = QHBoxLayout()

            self._card_emission = CardWidget(self)
            self._card_emission.setFixedHeight(100)
            emission_col = QVBoxLayout(self._card_emission)
            self._lbl_emission_title = BodyLabel("Emisi Hari Ini", self)
            self._lbl_emission_value = TitleLabel("0 kg CO2e", self)
            emission_col.addWidget(self._lbl_emission_title)
            emission_col.addWidget(self._lbl_emission_value)

            self._card_target = CardWidget(self)
            self._card_target.setFixedHeight(100)
            target_col = QVBoxLayout(self._card_target)

            target_title_row = QWidget(self)
            target_title_layout = QHBoxLayout(target_title_row)
            target_title_layout.setContentsMargins(0, 0, 0, 0)
            target_title_layout.setSpacing(4)

            self._lbl_target_title = BodyLabel("Target Harian", self)
            target_title_layout.addWidget(self._lbl_target_title)
            target_title_layout.addStretch()

            self._btn_edit_target = TransparentToolButton(FluentIcon.EDIT, self)
            self._btn_edit_target.setFixedSize(24, 24)
            self._btn_edit_target.setToolTip("Ubah Target")
            self._btn_edit_target.clicked.connect(self._on_edit_target_clicked)
            target_title_layout.addWidget(self._btn_edit_target)

            self._lbl_target_value = TitleLabel("0 kg CO2e", self)
            target_col.addWidget(target_title_row)
            target_col.addWidget(self._lbl_target_value)

            cards_layout.addWidget(self._card_emission, stretch=1)
            cards_layout.addWidget(self._card_target, stretch=1)
            self._main_layout.addLayout(cards_layout)

            self._chart = QChart()
            self._chart.setFont(QFont("Segoe UI", 9))
            self._chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

            self._chart_view = QChartView(self._chart)
            self._chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
            self._chart_view.setMinimumHeight(280)
            self._main_layout.addWidget(self._chart_view, 1)

            self._pivot.setCurrentItem("Harian")

        def _on_mode_changed(self, mode: str) -> None:
            self._current_mode = mode
            if mode == "Mingguan":
                self._current_date -= timedelta(days=self._current_date.weekday())
            self._load_data()

        def _on_prev_clicked(self) -> None:
            if self._current_mode == "Harian":
                self._current_date -= timedelta(days=1)
            else:
                self._current_date -= timedelta(days=7)
            self._load_data()

        def _on_next_clicked(self) -> None:
            if self._current_mode == "Harian":
                self._current_date += timedelta(days=1)
            else:
                self._current_date += timedelta(days=7)
            self._load_data()

        def _get_week_range(self) -> Tuple[datetime, datetime]:
            d = self._current_date.date()
            start = datetime.combine(d - timedelta(days=d.weekday()), time.min)
            end = datetime.combine(d + timedelta(days=6 - d.weekday()), time.max)
            return start, end

        @staticmethod
        def _start_of_day(dt: datetime) -> datetime:
            return datetime.combine(dt.date(), time.min)

        @staticmethod
        def _end_of_day(dt: datetime) -> datetime:
            return datetime.combine(dt.date(), time.max)

        def _update_date_label(self) -> None:
            if self._current_mode == "Harian":
                self._date_label.setText(self._current_date.strftime("%d %B %Y"))
                return

            week_start, _ = self._get_week_range()
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
                _, week_end = self._get_week_range()
                label_text = (
                    f"{week_start.strftime('%d %b %Y')}"
                    f" - {week_end.strftime('%d %b %Y')}"
                )
            self._date_label.setText(label_text)

        def _update_card_labels(self) -> None:
            if self._current_mode == "Harian":
                self._lbl_emission_title.setText("Emisi Hari Ini")
                self._lbl_target_title.setText("Target Harian")
            else:
                self._lbl_emission_title.setText("Emisi Minggu Ini")
                self._lbl_target_title.setText("Target Minggu Ini")

        def _update_chart(self) -> None:
            self._chart.setTitle(
                "Grafik Emisi Harian"
                if self._current_mode == "Harian"
                else "Grafik Emisi Mingguan"
            )
            self._chart.removeAllSeries()
            for axis in self._chart.axes():
                self._chart.removeAxis(axis)

            series = QBarSeries()
            bar_set = QBarSet("Emisi")
            categories: List[str] = []
            max_val = 0.0

            if self._current_mode == "Harian":
                week_start, week_end = self._get_week_range()
                summary: Dict = SummaryController.get_summary(week_start, week_end)
                values_by_date: Dict = {
                    d.date(): val
                    for d, val in summary.get("daily_emissions", [])
                }
                for i in range(7):
                    day = week_start + timedelta(days=i)
                    val = values_by_date.get(day.date(), 0.0)
                    bar_set.append(val)
                    categories.append(day.strftime("%a"))
                    if val > max_val:
                        max_val = val
            else:
                d = self._current_date.date()
                current_week_start = datetime.combine(
                    d - timedelta(days=d.weekday()), time.min
                )
                num_weeks = 8
                first_week_start = current_week_start - timedelta(weeks=num_weeks - 1)
                overall_end = datetime.combine(
                    d + timedelta(days=6 - d.weekday()), time.max
                )
                summary = SummaryController.get_summary(first_week_start, overall_end)
                values_by_week: Dict = {}
                for d_item, val in summary.get("daily_emissions", []):
                    wk_start = d_item - timedelta(days=d_item.weekday())
                    values_by_week[wk_start.date()] = (
                        values_by_week.get(wk_start.date(), 0.0) + val
                    )
                for i in range(num_weeks):
                    wk_start = first_week_start + timedelta(weeks=i)
                    val = values_by_week.get(wk_start.date(), 0.0)
                    bar_set.append(val)
                    categories.append(wk_start.strftime("%d %b"))
                    if val > max_val:
                        max_val = val

            series.append(bar_set)
            self._chart.addSeries(series)

            axis_x = QBarCategoryAxis()
            axis_x.append(categories)
            axis_x.setLabelsAngle(-30)
            axis_x.setLabelsFont(QFont("Segoe UI", 9))
            self._chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
            series.attachAxis(axis_x)

            axis_y = QValueAxis()
            axis_y.setTitleText("kg CO2e")
            axis_y.setRange(0, max_val * 1.2 if max_val > 0 else 10)
            axis_y.setLabelsFont(QFont("Segoe UI", 9))
            self._chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
            series.attachAxis(axis_y)

        def _load_data(self) -> None:
            self._update_date_label()
            self._update_card_labels()
            self._update_chart()

            week_start, week_end = self._get_week_range()
            if self._current_mode == "Harian":
                summary = SummaryController.get_summary(
                    self._start_of_day(self._current_date),
                    self._end_of_day(self._current_date),
                )
            else:
                summary = SummaryController.get_summary(week_start, week_end)

            total_emission: float = summary.get("total_emission", 0.0)
            target_emission: float = summary.get("target_emission", 0.0)

            self._lbl_emission_value.setText(f"{total_emission:.2f} kg CO2e")
            self._lbl_target_value.setText(f"{target_emission:.2f} kg CO2e")

            if target_emission > 0 and total_emission > target_emission:
                self._lbl_emission_value.setStyleSheet("color: red;")
            else:
                self._lbl_emission_value.setStyleSheet("color: green;")

        def _on_edit_target_clicked(self) -> None:
            modal = EmissionTargetFormView(self.window())
            modal.target_saved.connect(self.refresh)
            modal.open()
            self.window().titleBar.raise_()

    class _ActivityLogSection(QWidget):
        data_changed = pyqtSignal()

        def __init__(self, parent: Optional[QWidget] = None) -> None:
            super().__init__(parent)
            self._setup_widgets()
            self._setup_layout()
            self._connect_signals()
            self._load_logs()

        def refresh(self) -> None:
            self._load_logs()

        def _setup_widgets(self) -> None:
            self._btn_add = PrimaryPushButton(FluentIcon.ADD, "Tambah Log")
            self._btn_add.setFixedHeight(40)

            self._table = TableWidget(self)
            self._table.setColumnCount(6)
            self._table.setHorizontalHeaderLabels(
                ["ID", "Tanggal", "Kategori", "Besaran", "Satuan",
                 "Total Emisi (kg CO2e)"]
            )
            self._table.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeMode.Stretch
            )
            self._table.hideColumn(0)
            self._table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self._table.setSelectionBehavior(
                QAbstractItemView.SelectionBehavior.SelectRows
            )
            self._table.setAlternatingRowColors(True)
            self._table.verticalHeader().setVisible(False)
            self._table.setMinimumHeight(300)

            self._btn_edit = PushButton(FluentIcon.EDIT, "Edit")
            self._btn_delete = PushButton(FluentIcon.DELETE, "Hapus")
            self._btn_edit.setEnabled(False)
            self._btn_delete.setEnabled(False)
            self._btn_edit.setFixedHeight(40)
            self._btn_delete.setFixedHeight(40)

        def _setup_layout(self) -> None:
            title_row = QHBoxLayout()
            title_row.addWidget(SubtitleLabel("Aktivitas Terbaru", self))
            title_row.addStretch()
            title_row.addWidget(self._btn_add)

            action_row = QHBoxLayout()
            action_row.addWidget(self._btn_edit)
            action_row.addWidget(self._btn_delete)
            action_row.addStretch()

            root = QVBoxLayout(self)
            root.setContentsMargins(0, 0, 0, 0)
            root.setSpacing(12)
            root.addLayout(title_row)
            root.addLayout(action_row)
            root.addWidget(self._table)

        def _connect_signals(self) -> None:
            self._btn_add.clicked.connect(self._on_add_clicked)
            self._btn_edit.clicked.connect(self._on_edit_clicked)
            self._btn_delete.clicked.connect(self._on_delete_clicked)
            self._table.itemSelectionChanged.connect(self._on_selection_changed)

        def _on_selection_changed(self) -> None:
            selected = len(self._table.selectedItems()) > 0
            self._btn_edit.setEnabled(selected)
            self._btn_delete.setEnabled(selected)

        def _on_add_clicked(self) -> None:
            dialog = ActivityLogFormView(parent=self.window())
            dialog.log_saved.connect(self._load_logs)
            dialog.open()
            self.window().titleBar.raise_()

        def _on_edit_clicked(self) -> None:
            log = self._get_selected_log()
            if log is None:
                return
            dialog = ActivityLogFormView(selected_log=log, parent=self.window())
            dialog.log_saved.connect(self._load_logs)
            dialog.open()
            self.window().titleBar.raise_()

        def _on_delete_clicked(self) -> None:
            log = self._get_selected_log()
            if log is None:
                return
            dlg = MessageBox(
                "Hapus Log",
                f"Yakin ingin menghapus log '{log.category}' "
                f"pada {log.date.strftime('%d %b %Y') if log.date else '-'}?",
                self.window(),
            )
            if dlg.exec():
                ActivityLogController.delete_log(log.id or 0)
                self._load_logs()
                InfoBar.success(
                    title="Dihapus",
                    content="Log aktivitas berhasil dihapus.",
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    duration=3000,
                    position=InfoBarPosition.TOP,
                    parent=self.window(),
                )

        def _get_selected_log(self) -> Optional[ActivityLog]:
            row = self._table.currentRow()
            if row < 0:
                return None
            id_item = self._table.item(row, 0)
            if id_item is None:
                return None
            return id_item.data(Qt.ItemDataRole.UserRole)  # type: ignore[return-value]

        def _load_logs(self) -> None:
            logs: List[ActivityLog] = ActivityLogController.get_all_logs()
            self._table.setRowCount(0)

            for log in logs:
                row = self._table.rowCount()
                self._table.insertRow(row)

                id_item = QTableWidgetItem(str(log.id))
                id_item.setData(Qt.ItemDataRole.UserRole, log)
                id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                date_str = log.date.strftime("%d %b %Y") if log.date else "-"
                emission_str = (
                    f"{log.total_emission:.2f}"
                    if log.total_emission is not None
                    else "-"
                )

                items = [
                    id_item,
                    QTableWidgetItem(date_str),
                    QTableWidgetItem(log.category or "-"),
                    QTableWidgetItem(str(log.activity_value or "-")),
                    QTableWidgetItem(log.activity_unit or "-"),
                    QTableWidgetItem(emission_str),
                ]

                for col, item in enumerate(items):
                    if col > 0:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self._table.setItem(row, col, item)

            self._btn_edit.setEnabled(False)
            self._btn_delete.setEnabled(False)
            self.data_changed.emit()
