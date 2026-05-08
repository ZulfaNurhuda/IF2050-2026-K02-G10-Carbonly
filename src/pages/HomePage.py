from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QScrollArea, QVBoxLayout, QWidget
from qfluentwidgets import (
    BodyLabel,
    CardWidget,
    FluentIcon,
    StrongBodyLabel,
    SubtitleLabel,
    TitleLabel,
    ToolButton,
)

from src.services.AuthService import AuthService


class _AppHeader(CardWidget):
    profile_clicked = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(64)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 16, 0)
        layout.setSpacing(12)

        # SPEC FIX: wireframe labels this "Ini Branding/Logo Carbonly" — using text
        # placeholder until a logo asset is provided
        branding = StrongBodyLabel("Carbonly", self)
        branding.setStyleSheet("font-size: 16px;")

        self._profile_btn = ToolButton(FluentIcon.PEOPLE, self)
        self._profile_btn.setFixedSize(36, 36)
        self._profile_btn.clicked.connect(self.profile_clicked)

        layout.addWidget(branding)
        layout.addStretch(1)
        layout.addWidget(self._profile_btn)


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
        layout.addWidget(TitleLabel(value, self))
        unit_lbl = BodyLabel(unit, self)
        unit_lbl.setStyleSheet("color: gray;")
        layout.addWidget(unit_lbl)


class HomePage(QWidget):
    profile_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("home-page")
        self._welcome_label: TitleLabel | None = None
        self._setup_ui()

    def refresh(self) -> None:
        if self._welcome_label is not None:
            user = AuthService.get_current_user()
            username = user.username if user else "Pengguna"
            self._welcome_label.setText(f"Selamat datang, {username}!")

    def _setup_ui(self) -> None:
        user = AuthService.get_current_user()
        username = user.username if user else "Pengguna"

        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(16)

        # ─── In-app header (fixed, non-scrolling) ───
        header = _AppHeader(self)
        header.profile_clicked.connect(self.profile_requested)
        outer.addWidget(header)

        # ─── Scrollable content area ───
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(4, 8, 4, 8)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Welcome
        self._welcome_label = TitleLabel(f"Selamat datang, {username}!", content)
        desc = BodyLabel("Pantau jejak karbon harian kamu di sini.", content)
        desc.setStyleSheet("color: gray;")
        layout.addWidget(self._welcome_label)
        layout.addWidget(desc)

        # Summary stat cards
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

        # Recent activity section
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
