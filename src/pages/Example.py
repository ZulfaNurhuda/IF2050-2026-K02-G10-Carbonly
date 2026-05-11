from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    PrimaryPushButton,
    StrongBodyLabel,
    SubtitleLabel,
    TitleLabel,
    setFont,
)

from src.controllers.TargetEmisiController import TargetEmisiController
from src.views.FormTargetView import FormTargetView


class ExamplePage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("example-page")

        self._controller = TargetEmisiController()
        self._setup_ui()
        self._refresh()

    # ------------------------------------------------------------------ #
    # UI                                                                   #
    # ------------------------------------------------------------------ #

    def _setup_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(36, 32, 36, 32)
        root.setSpacing(24)

        # Page title
        title = TitleLabel("Target Emisi", self)
        setFont(title, 28)
        root.addWidget(title)

        # Card
        card = CardWidget(self)
        card.setFixedWidth(420)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 24, 28, 24)
        card_layout.setSpacing(12)

        # Label
        lbl_field = StrongBodyLabel("Nilai Target Emisi Harian", card)
        card_layout.addWidget(lbl_field)

        # Value row: [big number] [satuan]
        value_row = QWidget(card)
        value_layout = QHBoxLayout(value_row)
        value_layout.setContentsMargins(0, 0, 0, 0)
        value_layout.setSpacing(8)
        value_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self._value_label = TitleLabel("—", value_row)
        setFont(self._value_label, 36)

        self._satuan_label = SubtitleLabel("kg CO\u2082e", value_row)
        self._satuan_label.setAlignment(Qt.AlignmentFlag.AlignBottom)

        value_layout.addWidget(self._value_label)
        value_layout.addWidget(self._satuan_label)
        card_layout.addWidget(value_row)

        # Info note
        info = BodyLabel(
            "Target berlaku secara global kepada seluruh riwayat.", card
        )
        info.setStyleSheet("color: #007f7f;")
        info.setWordWrap(True)
        card_layout.addWidget(info)

        card_layout.addSpacing(8)

        # Edit button
        self._edit_btn = PrimaryPushButton("Ubah Target", card)
        self._edit_btn.setFixedHeight(40)
        self._edit_btn.clicked.connect(self._open_modal)
        card_layout.addWidget(self._edit_btn)

        root.addWidget(card)
        root.addStretch()

    # ------------------------------------------------------------------ #
    # Logic                                                                #
    # ------------------------------------------------------------------ #

    def _refresh(self) -> None:
        """Pull the latest target from the DB and update the display."""
        target = self._controller.dapatkanTarget()
        if target and target.nilaiTarget is not None:
            self._value_label.setText(str(target.nilaiTarget))
        else:
            self._value_label.setText("Belum diatur")

    def _open_modal(self) -> None:
        """Open the FormTargetView modal and refresh on success."""
        modal = FormTargetView(self)
        modal.target_disimpan.connect(self._refresh)
        modal.exec()