# ruff: noqa
# flake8: noqa
# mypy: ignore-errors
from datetime import datetime
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QWidget
from qfluentwidgets import (
    BodyLabel,
    LineEdit,
    MessageBoxBase,
    PrimaryPushButton,
    StrongBodyLabel,
    InfoBar,
    InfoBarPosition,
)

from src.controllers.TargetEmisiController import TargetEmisiController
from src.models.TargetEmisi import TargetEmisi


class FormTargetView(MessageBoxBase):
    """Modal dialog for setting / editing the daily emission target (UC06, UC07).

    Shows one input field: the target value in kg CO₂e.
    Emits ``target_disimpan`` after a successful save so the parent widget
    can refresh its display.
    """

    target_disimpan = pyqtSignal()

    # ------------------------------------------------------------------ #
    # Construction                                                         #
    # ------------------------------------------------------------------ #

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Target Emisi Harian")

        # Stub-compatible attributes
        self._controller: TargetEmisiController = TargetEmisiController()
        self._inputNilaiTarget: Optional[float] = None
        self._inputSatuan: str = "kg CO\u2082e"
        self._inputTahun: int = datetime.now().year

        self._setup_ui()

        # Hide the default yes/cancel buttons
        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.buttonGroup.setFixedHeight(0)

        # Pre-fill with the existing target, if any
        self.tampilkan()

    # ------------------------------------------------------------------ #
    # Properties (stub-compatible)                                         #
    # ------------------------------------------------------------------ #

    @property
    def controller(self) -> TargetEmisiController:
        return self._controller

    @controller.setter
    def controller(self, value: TargetEmisiController) -> None:
        self._controller = value

    @property
    def inputNilaiTarget(self) -> Optional[float]:
        return self._inputNilaiTarget

    @inputNilaiTarget.setter
    def inputNilaiTarget(self, value: float) -> None:
        self._inputNilaiTarget = value

    @property
    def inputSatuan(self) -> str:
        return self._inputSatuan

    @inputSatuan.setter
    def inputSatuan(self, value: str) -> None:
        self._inputSatuan = value

    @property
    def inputTahun(self) -> int:
        return self._inputTahun

    @inputTahun.setter
    def inputTahun(self, value: int) -> None:
        self._inputTahun = value

    # ------------------------------------------------------------------ #
    # UI setup                                                             #
    # ------------------------------------------------------------------ #

    def _setup_ui(self) -> None:
        # Title
        self._title_label = StrongBodyLabel("Ubah Target Emisi Harian", self)
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Input row: [LineEdit] [kg CO₂e label]
        self._input_row = QWidget(self)
        row_layout = QHBoxLayout(self._input_row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(8)

        self._nilai_input = LineEdit(self)
        self._nilai_input.setPlaceholderText("Contoh: 8.5")
        self._nilai_input.setFixedHeight(40)
        self._nilai_input.setFixedWidth(220)

        self._satuan_label = BodyLabel(self._inputSatuan, self)
        self._satuan_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        row_layout.addWidget(self._nilai_input)
        row_layout.addWidget(self._satuan_label)
        row_layout.addStretch()

        # Informational note
        self._info_label = BodyLabel(
            "Target berlaku secara global kepada seluruh riwayat.", self
        )
        self._info_label.setStyleSheet("color: #007f7f;")
        self._info_label.setWordWrap(True)

        # Error label (hidden by default)
        self._error_label = StrongBodyLabel("", self)
        self._error_label.setStyleSheet("color: red;")
        self._error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._error_label.setVisible(False)

        # Action buttons
        self._btn_row = QWidget(self)
        btn_layout = QHBoxLayout(self._btn_row)
        btn_layout.setContentsMargins(0, 8, 0, 0)
        btn_layout.setSpacing(8)
        btn_layout.addStretch()

        self._batal_btn = LineEdit(self)   # placeholder – replaced below
        # Use a plain PushButton for Batal and PrimaryPushButton for Simpan
        from PyQt6.QtWidgets import QPushButton
        self._batal_btn = QPushButton("Batal", self)
        self._batal_btn.setFixedHeight(36)
        self._batal_btn.setMinimumWidth(80)
        self._batal_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background: transparent;
                font-size: 14px;
            }
            QPushButton:hover { background: rgba(0,0,0,0.05); }
        """)
        self._batal_btn.clicked.connect(self.reject)

        self._simpan_btn = PrimaryPushButton("Simpan", self)
        self._simpan_btn.setFixedHeight(36)
        self._simpan_btn.setMinimumWidth(80)
        self._simpan_btn.clicked.connect(self.simpanForm)

        btn_layout.addWidget(self._batal_btn)
        btn_layout.addWidget(self._simpan_btn)

        # Assemble into viewLayout
        self.viewLayout.addWidget(self._title_label)
        self.viewLayout.addSpacing(8)
        self.viewLayout.addWidget(self._input_row)
        self.viewLayout.addWidget(self._info_label)
        self.viewLayout.addSpacing(4)
        self.viewLayout.addWidget(self._error_label)
        self.viewLayout.addWidget(self._btn_row)

        self.widget.setMinimumWidth(360)

    # ------------------------------------------------------------------ #
    # Public interface (matches DPPL spec + stub)                          #
    # ------------------------------------------------------------------ #

    def tampilkan(self) -> None:
        """Load the current target from DB and pre-fill the form."""
        target = self._controller.dapatkanTarget()
        if target:
            self.fillForm(target)

    def fillForm(self, targetData: TargetEmisi) -> None:
        """Populate the input field with an existing TargetEmisi."""
        if targetData.nilaiTarget is not None:
            self._nilai_input.setText(str(targetData.nilaiTarget))
        self._inputNilaiTarget = targetData.nilaiTarget
        self._inputSatuan = targetData.satuan or "kg CO\u2082e"
        self._inputTahun = targetData.tahun or datetime.now().year

    def simpanForm(self) -> None:
        """Read the input field, validate, and persist via the controller."""
        raw = self._nilai_input.text().strip().replace(",", ".")
        if not raw:
            self.tampilkanError("Nilai target tidak boleh kosong.")
            return

        try:
            nilai = float(raw)
        except ValueError:
            self.tampilkanError("Masukkan angka yang valid (contoh: 8.5).")
            return

        if nilai <= 0:
            self.tampilkanError("Nilai target harus lebih dari 0.")
            return
        
        if nilai < 0.1 and nilai != 0:
            self.tampilkanError("Nilai target terlalu rendah. Pastikan nilainya realistis.")
            return

        if nilai > 20:
            self.tampilkanError("Nilai target terlalu tinggi. Pastikan nilainya realistis.")
            return

        data = TargetEmisi(
            nilaiTarget=nilai,
            satuan=self._inputSatuan,
            tahun=self._inputTahun or datetime.now().year,
        )

        ok, pesan = self._controller.simpanTarget(data)
        if ok:
            self.tampilkanSukses()
        else:
            self.tampilkanError(pesan)

    def tampilkanError(self, pesan: str) -> None:
        """Show an inline error message."""
        self._error_label.setText(pesan)
        self._error_label.setVisible(True)

    def tampilkanSukses(self) -> None:
        """Notify success, emit signal, and close the dialog."""
        self._error_label.setVisible(False)
        self.target_disimpan.emit()
        self.accept()