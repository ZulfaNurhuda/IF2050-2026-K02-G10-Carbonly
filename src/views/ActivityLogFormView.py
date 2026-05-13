from datetime import datetime
from typing import Optional

from PyQt6 import QtCore
from PyQt6.QtCore import QDate, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QFormLayout, QHBoxLayout, QPushButton, QWidget
from qfluentwidgets import (
    BodyLabel,
    CalendarPicker,
    ComboBox,
    DoubleSpinBox,
    FluentIcon,
    MessageBoxBase,
    PrimaryPushButton,
    PushButton,
    StrongBodyLabel,
    TitleLabel,
    setFont,
)

from src.controllers.ActivityLogController import ActivityLogController
from src.models.ActivityLog import ActivityLog

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
        self.setWindowTitle("Log Aktivitas Karbon")

        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.buttonGroup.setFixedHeight(0)

        self._setup_close_button()
        self._setup_widgets()
        self._setup_layout()
        self._connect_signals()

        if selected_log is not None:
            self.fill_form(selected_log)

        self.widget.setMinimumWidth(460)

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
        self._lbl_title = TitleLabel("Catat Aktivitas Karbon")
        setFont(self._lbl_title, 18)

        self._lbl_category = BodyLabel("Kategori Aktivitas")
        self._cb_category = ComboBox()
        self._cb_category.addItems(CATEGORY_LIST)

        self._lbl_date = BodyLabel("Tanggal")
        self._date_picker = CalendarPicker()
        self._date_picker.setDate(QDate.currentDate())

        self._lbl_value = BodyLabel("Besaran Aktivitas")
        self._spin_value = DoubleSpinBox()
        self._spin_value.setRange(0.01, 999_999.99)
        self._spin_value.setDecimals(2)
        self._spin_value.setSingleStep(1.0)

        self._msg_label = StrongBodyLabel("", self)
        self._msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._msg_label.setVisible(False)

        self._btn_save = PrimaryPushButton(FluentIcon.SAVE, "Simpan")
        self._btn_cancel = PushButton(FluentIcon.CLOSE, "Batal")
        self._btn_save.setFixedWidth(120)
        self._btn_cancel.setFixedWidth(120)

    def _setup_layout(self) -> None:
        form_layout = QFormLayout()
        form_layout.setSpacing(14)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.addRow(self._lbl_category, self._cb_category)
        form_layout.addRow(self._lbl_date, self._date_picker)
        form_layout.addRow(self._lbl_value, self._spin_value)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self._btn_cancel)
        btn_row.addWidget(self._btn_save)

        self.viewLayout.setContentsMargins(32, 28, 32, 24)
        self.viewLayout.setSpacing(20)
        self.viewLayout.addWidget(self._lbl_title)
        self.viewLayout.addLayout(form_layout)
        self.viewLayout.addWidget(self._msg_label)
        self.viewLayout.addSpacing(4)
        self.viewLayout.addLayout(btn_row)

    def _connect_signals(self) -> None:
        self._btn_save.clicked.connect(self._on_save_clicked)
        self._btn_cancel.clicked.connect(self.reject)

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
        self._lbl_title.setText("Edit Aktivitas Karbon")

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
        self._lbl_title.setText("Catat Aktivitas Karbon")

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
