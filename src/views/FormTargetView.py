# ruff: noqa
# flake8: noqa
# mypy: ignore-errors
from datetime import datetime
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QFormLayout, QWidget
from qfluentwidgets import (
    BodyLabel,
    LineEdit,
    MessageBoxBase,
    PrimaryPushButton,
    PushButton,
    TitleLabel,
    FluentIcon,
    InfoBar,
    InfoBarPosition,
    setFont,
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

        self._buatWidget()
        self._buatLayout()
        self._hubungkanSinyal()

        # Hide the default yes/cancel buttons
        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.buttonGroup.setFixedHeight(0)

        self.widget.setMinimumWidth(460)

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

    def _buatWidget(self) -> None:
        self._lblJudul = TitleLabel("Ubah Target Emisi Harian")
        setFont(self._lblJudul, 18)

        self._lblNilaiTarget = BodyLabel("Nilai Target")

        self._nilai_input = LineEdit()
        self._nilai_input.setPlaceholderText("Contoh: 8.5")
        self._nilai_input.setFixedHeight(40)

        self._satuan_label = BodyLabel(self._inputSatuan)
        self._satuan_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._btnSimpan = PrimaryPushButton(FluentIcon.SAVE, "Simpan")
        self._btnBatal = PushButton(FluentIcon.CLOSE, "Batal")
        self._btnSimpan.setFixedWidth(120)
        self._btnBatal.setFixedWidth(120)

    def _buatLayout(self) -> None:
        # Input row: [LineEdit] [kg CO₂e label]
        input_row = QWidget()
        input_layout = QHBoxLayout(input_row)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)
        input_layout.addWidget(self._nilai_input)
        input_layout.addWidget(self._satuan_label)

        formLayout = QFormLayout()
        formLayout.setSpacing(14)
        formLayout.setContentsMargins(0, 0, 0, 0)
        formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        formLayout.addRow(self._lblNilaiTarget, input_row)

        btnLayout = QHBoxLayout()
        btnLayout.addStretch()
        btnLayout.addWidget(self._btnBatal)
        btnLayout.addWidget(self._btnSimpan)

        self.viewLayout.setContentsMargins(32, 28, 32, 24)
        self.viewLayout.setSpacing(20)
        self.viewLayout.addWidget(self._lblJudul)
        self.viewLayout.addLayout(formLayout)
        self.viewLayout.addSpacing(8)
        self.viewLayout.addLayout(btnLayout)

    def _hubungkanSinyal(self) -> None:
        self._btnSimpan.clicked.connect(self.simpanForm)
        self._btnBatal.clicked.connect(self.reject)

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
        """Show an error InfoBar at the top of the dialog."""
        InfoBar.error(
            title="Gagal Menyimpan",
            content=pesan,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=4000,
            position=InfoBarPosition.TOP,
            parent=self,
        )

    def tampilkanSukses(self) -> None:
        """Notify success, emit signal, and close the dialog."""
        InfoBar.success(
            title="Berhasil Disimpan",
            content="Target emisi harian berhasil disimpan.",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=3000,
            position=InfoBarPosition.TOP,
            parent=self.parent(),
        )
        self.target_disimpan.emit()
        self.accept()