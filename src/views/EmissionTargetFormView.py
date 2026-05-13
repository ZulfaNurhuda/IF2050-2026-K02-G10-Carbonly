from datetime import datetime
from typing import Optional

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QFormLayout, QHBoxLayout, QPushButton, QWidget
from qfluentwidgets import (
    BodyLabel,
    FluentIcon,
    LineEdit,
    MessageBoxBase,
    PrimaryPushButton,
    PushButton,
    StrongBodyLabel,
    TitleLabel,
    setFont,
)

from src.controllers.EmissionTargetController import EmissionTargetController
from src.models.EmissionTarget import EmissionTarget


class EmissionTargetFormView(MessageBoxBase):
    target_saved = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Target Emisi Harian")

        self._unit: str = "kg CO₂e"
        self._year: int = datetime.now().year

        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.buttonGroup.setFixedHeight(0)

        self._setup_close_button()
        self._setup_widgets()
        self._setup_layout()
        self._connect_signals()

        self.widget.setMinimumWidth(460)
        self._prefill_from_db()

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
        self._lbl_title = TitleLabel("Ubah Target Emisi Harian")
        setFont(self._lbl_title, 18)

        self._lbl_value = BodyLabel("Nilai Target")

        self._value_input = LineEdit()
        self._value_input.setPlaceholderText("Contoh: 8.5")
        self._value_input.setFixedHeight(40)

        self._unit_label = BodyLabel(self._unit)
        self._unit_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._msg_label = StrongBodyLabel("", self)
        self._msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._msg_label.setVisible(False)

        self._btn_save = PrimaryPushButton(FluentIcon.SAVE, "Simpan")
        self._btn_cancel = PushButton(FluentIcon.CLOSE, "Batal")
        self._btn_save.setFixedWidth(120)
        self._btn_cancel.setFixedWidth(120)

    def _setup_layout(self) -> None:
        input_row_widget = QWidget()
        input_row = QHBoxLayout(input_row_widget)
        input_row.setContentsMargins(0, 0, 0, 0)
        input_row.setSpacing(8)
        input_row.addWidget(self._value_input)
        input_row.addWidget(self._unit_label)

        form_layout = QFormLayout()
        form_layout.setSpacing(14)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.addRow(self._lbl_value, input_row_widget)

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
        self._value_input.returnPressed.connect(self._on_save_clicked)

    def _prefill_from_db(self) -> None:
        target = EmissionTargetController.get_target()
        if target and target.target_value is not None:
            self._value_input.setText(str(target.target_value))
            self._unit = target.unit or "kg CO₂e"
            self._year = target.year or datetime.now().year

    def _on_save_clicked(self) -> None:
        raw = self._value_input.text().strip().replace(",", ".")
        if not raw:
            self._set_msg("Nilai target tidak boleh kosong.", error=True)
            return

        try:
            value = float(raw)
        except ValueError:
            self._set_msg("Masukkan angka yang valid (contoh: 8.5).", error=True)
            return

        if value <= 0:
            self._set_msg("Nilai target harus lebih dari 0.", error=True)
            return

        if value < 0.1:
            self._set_msg(
                "Nilai target terlalu rendah. Pastikan nilainya realistis.",
                error=True,
            )
            return

        if value > 20:
            self._set_msg(
                "Nilai target terlalu tinggi. Pastikan nilainya realistis.",
                error=True,
            )
            return

        data = EmissionTarget(
            target_value=value,
            unit=self._unit,
            year=self._year or datetime.now().year,
        )

        ok, message = EmissionTargetController.save_target(data)
        if ok:
            self.target_saved.emit()
            self.accept()
        else:
            self._set_msg(message, error=True)

    def _set_msg(self, message: str, *, error: bool) -> None:
        self._msg_label.setStyleSheet(f"color: {'red' if error else 'green'};")
        self._msg_label.setText(message)
        self._msg_label.setVisible(True)
