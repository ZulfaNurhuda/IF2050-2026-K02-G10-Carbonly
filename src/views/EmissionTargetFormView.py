from datetime import datetime
from typing import Optional

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget
from qfluentwidgets import (
    BodyLabel,
    FluentIcon,
    LineEdit,
    MessageBoxBase,
    PrimaryPushButton,
    StrongBodyLabel,
    SubtitleLabel,
)

from src.controllers.EmissionTargetController import EmissionTargetController
from src.models.EmissionTarget import EmissionTarget


class EmissionTargetFormView(MessageBoxBase):
    target_saved = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Ubah Target Emisi Harian")

        self._unit: str = "kg CO₂e"
        self._year: int = datetime.now().year

        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.buttonGroup.setFixedHeight(0)

        self._setup_close_button()
        self._setup_widgets()
        self._setup_layout()
        self._connect_signals()

        self.widget.setMinimumWidth(400)
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
        self.viewLayout.addWidget(SubtitleLabel("Ubah Target Emisi Harian", self))

        self._lbl_value = StrongBodyLabel("Nilai Target", self)

        self._value_input = LineEdit(self)
        self._value_input.setPlaceholderText("Contoh: 8.5")
        self._value_input.setFixedHeight(40)

        self._unit_label = BodyLabel(self._unit, self)
        self._unit_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._msg_label = StrongBodyLabel("", self)
        self._msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._msg_label.setVisible(False)

        self._btn_save = PrimaryPushButton("Simpan", self)
        self._btn_save.setFixedHeight(40)
        self._btn_save.setMinimumWidth(300)

    def _setup_layout(self) -> None:
        input_row = QHBoxLayout()
        input_row.setContentsMargins(0, 0, 0, 0)
        input_row.setSpacing(8)
        input_row.addWidget(self._value_input)
        input_row.addWidget(self._unit_label)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(0, 0, 0, 0)
        btn_row.setSpacing(8)
        btn_row.addWidget(self._btn_save)
        btn_row.addStretch(1)

        self.viewLayout.addWidget(self._lbl_value)
        self.viewLayout.addLayout(input_row)
        self.viewLayout.addWidget(self._msg_label)
        self.viewLayout.addLayout(btn_row)

    def _connect_signals(self) -> None:
        self._btn_save.clicked.connect(self._on_save_clicked)
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
