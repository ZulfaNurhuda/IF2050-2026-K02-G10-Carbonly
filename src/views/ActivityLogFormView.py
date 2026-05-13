from datetime import datetime
from typing import Optional

from PyQt6 import QtCore
from PyQt6.QtCore import QDate, QPoint, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget
from qfluentwidgets import (
    CalendarPicker,
    ComboBox,
    DoubleSpinBox,
    FluentIcon,
    MenuAnimationType,
    MessageBoxBase,
    PrimaryPushButton,
    StrongBodyLabel,
    SubtitleLabel,
)
from qfluentwidgets.components.date_time.calendar_view import CalendarView
from qfluentwidgets.components.widgets.combo_box import ComboBoxMenu

from src.controllers.ActivityLogController import ActivityLogController
from src.models.ActivityLog import ActivityLog


class _FlatComboBoxMenu(ComboBoxMenu):
    def exec(self, pos, **_):
        return super().exec(pos, aniType=MenuAnimationType.NONE)


class _FlatCalendarView(CalendarView):
    def exec(self, pos, **_):
        return super().exec(pos, ani=False)


class _FlatComboBox(ComboBox):
    def _createComboMenu(self):  # noqa: N802
        menu = _FlatComboBoxMenu(self)
        menu.view.setGraphicsEffect(None)
        menu.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        return menu


class _FlatCalendarPicker(CalendarPicker):
    def _showCalendarView(self):  # noqa: N802
        view = _FlatCalendarView(self.window())
        view.setResetEnabled(self.isRestEnabled())
        view.stackedWidget.setGraphicsEffect(None)
        view.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        view.resetted.connect(self.reset)
        view.dateChanged.connect(self._onDateChanged)
        if self._date.isValid():
            view.setDate(self._date)
        x = int(self.width() / 2 - view.sizeHint().width() / 2)
        y = self.height()
        view.exec(self.mapToGlobal(QPoint(x, y)))


UNIT_MAP = {
    "Transportasi": "km",
    "Listrik": "kWh",
    "Gas Alam": "m³",
    "Makanan": "kg",
    "Sampah": "kg",
}

CATEGORY_LIST = [f"{k} ({v})" for k, v in UNIT_MAP.items()]


class ActivityLogFormView(MessageBoxBase):
    log_saved = pyqtSignal()

    def __init__(
        self,
        selected_log: Optional[ActivityLog] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._selected_log = selected_log

        self.setObjectName("activity-log-form-dialog")
        self.setWindowTitle(
            "Edit Aktivitas Karbon"
            if selected_log is not None
            else "Catat Aktivitas Karbon"
        )

        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.buttonGroup.setFixedHeight(0)

        self._setup_close_button()
        self._setup_widgets()
        self._setup_layout()
        self._connect_signals()

        if selected_log is not None:
            self.fill_form(selected_log)

        self.widget.setMinimumWidth(400)

    def showEvent(self, event: QShowEvent) -> None:  # noqa: N802
        super().showEvent(event)
        if self.parent():
            QTimer.singleShot(0, self._adjust_geometry)

    def _adjust_geometry(self) -> None:
        if self.parent() and hasattr(self.parent(), "width"):
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())

    def _setup_close_button(self) -> None:
        self._close_btn = QPushButton(self.widget)
        self._close_btn.setFixedSize(24, 24)
        self._close_btn.setIcon(FluentIcon.CLOSE.icon())
        self._close_btn.setIconSize(QtCore.QSize(12, 12))
        self._close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)
        self._close_btn.clicked.connect(self.reject)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        row.addStretch(1)
        row.addWidget(self._close_btn)
        self.viewLayout.insertLayout(0, row)

    def _setup_widgets(self) -> None:
        self.viewLayout.addWidget(SubtitleLabel(self.windowTitle(), self))

        self._lbl_category = StrongBodyLabel("Kategori Aktivitas", self)
        self._cb_category = _FlatComboBox(self)
        self._cb_category.addItems(CATEGORY_LIST)
        self._cb_category.setFixedHeight(40)

        self._lbl_date = StrongBodyLabel("Tanggal", self)
        self._date_picker = _FlatCalendarPicker(self)
        self._date_picker.setDate(QDate.currentDate())
        self._date_picker.setFixedHeight(40)

        self._lbl_value = StrongBodyLabel("Besaran Aktivitas", self)
        self._spin_value = DoubleSpinBox(self)
        self._spin_value.setRange(0.01, 999_999.99)
        self._spin_value.setDecimals(2)
        self._spin_value.setSingleStep(1.0)
        self._spin_value.setFixedHeight(40)

        self._msg_label = StrongBodyLabel("", self)
        self._msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._msg_label.setVisible(False)

        self._btn_save = PrimaryPushButton("Simpan", self)
        self._btn_save.setFixedHeight(40)

    def _setup_layout(self) -> None:
        self.viewLayout.addWidget(self._lbl_category)
        self.viewLayout.addWidget(self._cb_category)
        self.viewLayout.addWidget(self._lbl_date)
        self.viewLayout.addWidget(self._date_picker)
        self.viewLayout.addWidget(self._lbl_value)
        self.viewLayout.addWidget(self._spin_value)
        self.viewLayout.addWidget(self._msg_label)
        self.viewLayout.addWidget(self._btn_save)

    def _connect_signals(self) -> None:
        self._btn_save.clicked.connect(self._on_save_clicked)

    @staticmethod
    def _parse_category(display_text: str) -> str:
        return display_text.split(" (")[0]

    @property
    def _input_category(self) -> Optional[str]:
        text = self._cb_category.currentText()
        return self._parse_category(text) if text else None

    @property
    def _input_date(self) -> Optional[datetime]:
        qdate: QDate = self._date_picker.getDate()
        if qdate.isValid():
            return datetime(qdate.year(), qdate.month(), qdate.day())
        return None

    @property
    def _input_value(self) -> Optional[float]:
        v = self._spin_value.value()
        return v if v > 0 else None

    @property
    def _input_unit(self) -> Optional[str]:
        category = self._input_category
        return UNIT_MAP.get(category) if category else None

    def fill_form(self, log_data: ActivityLog) -> None:
        self._selected_log = log_data
        self.setWindowTitle("Edit Aktivitas Karbon")

        display_text = f"{log_data.category or ''} ({log_data.activity_unit or ''})"
        idx = self._cb_category.findText(display_text)
        self._cb_category.setCurrentIndex(idx if idx >= 0 else 0)

        if log_data.date:
            qd = QDate(log_data.date.year, log_data.date.month, log_data.date.day)
            self._date_picker.setDate(qd)

        self._spin_value.setValue(log_data.activity_value or 0.0)

    def _reset_form(self) -> None:
        self._selected_log = None
        self._cb_category.setCurrentIndex(0)
        self._date_picker.setDate(QDate.currentDate())
        self._spin_value.setValue(0.0)
        self.setWindowTitle("Catat Aktivitas Karbon")

    def _on_save_clicked(self) -> None:
        data = ActivityLog(
            id=self._selected_log.id if self._selected_log else None,
            date=self._input_date,
            category=self._input_category,
            activity_value=self._input_value,
            activity_unit=self._input_unit,
        )

        ok = ActivityLogController.save_log(data)
        if ok:
            self.log_saved.emit()
            self._reset_form()
            self.accept()
        else:
            self._set_msg(
                "Pastikan semua field terisi dan besaran aktivitas lebih dari 0.",
                error=True,
            )

    def _set_msg(self, message: str, *, error: bool) -> None:
        self._msg_label.setStyleSheet(f"color: {'red' if error else 'green'};")
        self._msg_label.setText(message)
        self._msg_label.setVisible(True)
