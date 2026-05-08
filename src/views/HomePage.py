from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QScrollArea, QVBoxLayout, QWidget
from qfluentwidgets import (
    BodyLabel,
    CaptionLabel,
    CardWidget,
    FluentIcon,
    PrimaryPushButton,
    SubtitleLabel,
    TitleLabel,
    setFont,
    themeColor,
)

from src.controllers.AuthController import AuthController


class HomePage(QWidget):
    profile_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("home-page")
        self._welcome_label: SubtitleLabel | None = None
        self._header: HomePage._AppHeader | None = None
        self._setup_ui()

    def refresh(self) -> None:
        username = AuthController.get_current_username() or "Pengguna"
        if self._welcome_label is not None:
            self._welcome_label.setText(f"Selamat datang, {username}!")
        if self._header is not None:
            self._header.set_username(username)

    def _setup_ui(self) -> None:
        username = AuthController.get_current_username() or "Pengguna"

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(16)

        self._header = HomePage._AppHeader(self)
        self._header.profile_clicked.connect(self.profile_requested)
        outer.addWidget(self._header)

        # <!-- DUMMY, SILAKAN GANTI UNTUK YANG MENGIMPLEMENTASIKAN -->
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
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

        self._welcome_label = SubtitleLabel(f"Selamat datang, {username}!", content)
        desc = BodyLabel("Pantau jejak karbon harian kamu di sini.", content)
        desc.setStyleSheet("color: gray;")
        layout.addWidget(self._welcome_label)
        layout.addWidget(desc)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)
        for card_title, card_unit in [
            ("Emisi Hari Ini", "kg CO₂"),
            ("Target Emisi", "kg CO₂ / hari"),
            ("Aktivitas Bulan Ini", "log tercatat"),
        ]:
            card = CardWidget(content)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 16, 20, 16)
            card_layout.setSpacing(6)
            card_layout.addWidget(BodyLabel(card_title, card))
            value_lbl = TitleLabel("—", card)
            value_lbl.setStyleSheet(f"color: {themeColor().name()};")
            card_layout.addWidget(value_lbl)
            unit_lbl = BodyLabel(card_unit, card)
            unit_lbl.setStyleSheet("color: gray;")
            card_layout.addWidget(unit_lbl)
            cards_row.addWidget(card, 1)
        layout.addLayout(cards_row)

        layout.addWidget(SubtitleLabel("Aktivitas Terbaru", content))

        recent_card = CardWidget(content)
        recent_layout = QVBoxLayout(recent_card)
        recent_layout.setContentsMargins(20, 20, 20, 20)
        placeholder = BodyLabel(
            "Belum ada aktivitas tercatat.\n"
            "Buka menu Log Aktivitas untuk mulai mencatat.",
            recent_card,
        )
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: gray;")
        recent_layout.addWidget(placeholder)
        layout.addWidget(recent_card)

        layout.addStretch(1)
        scroll.setWidget(content)
        outer.addWidget(scroll)
        # <!-- BATAS DUMMY YANG BOLEH DIGANTI -->

    class _AppHeader(CardWidget):
        profile_clicked = pyqtSignal()

        def __init__(self, parent: QWidget | None = None) -> None:
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
