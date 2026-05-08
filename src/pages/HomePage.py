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

from src.services.AuthService import AuthService


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

        user = AuthService.get_current_user()
        username = (user.username or "") if user else ""
        self._profile_btn = PrimaryPushButton(FluentIcon.PEOPLE, username, self)
        self._profile_btn.clicked.connect(self.profile_clicked)

        outer.addLayout(branding_col)
        outer.addStretch(1)
        outer.addWidget(self._profile_btn)

    def set_username(self, username: str) -> None:
        self._profile_btn.setText(username)


class _StatCard(CardWidget):
    def __init__(
        self,
        title: str,
        value: str,
        unit: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)

        layout.addWidget(BodyLabel(title, self))

        value_lbl = TitleLabel(value, self)
        value_lbl.setStyleSheet(f"color: {themeColor().name()};")
        layout.addWidget(value_lbl)

        unit_lbl = BodyLabel(unit, self)
        unit_lbl.setStyleSheet("color: gray;")
        layout.addWidget(unit_lbl)


class HomePage(QWidget):
    profile_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("home-page")
        self._welcome_label: SubtitleLabel | None = None
        self._header: _AppHeader | None = None
        self._setup_ui()

    def refresh(self) -> None:
        user = AuthService.get_current_user()
        username = (user.username or "Pengguna") if user else "Pengguna"
        if self._welcome_label is not None:
            self._welcome_label.setText(f"Selamat datang, {username}!")
        if self._header is not None:
            self._header.set_username(username)

    def _setup_ui(self) -> None:
        user = AuthService.get_current_user()
        username = user.username if user else "Pengguna"

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(16)

        self._header = _AppHeader(self)
        self._header.profile_clicked.connect(self.profile_requested)
        outer.addWidget(self._header)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        scroll.viewport().setAutoFillBackground(False)

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
        cards_row.addWidget(
            _StatCard("Emisi Hari Ini", "—", "kg CO₂", content), 1
        )
        cards_row.addWidget(
            _StatCard("Target Emisi", "—", "kg CO₂ / hari", content), 1
        )
        cards_row.addWidget(
            _StatCard("Aktivitas Bulan Ini", "—", "log tercatat", content), 1
        )
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
