from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QScrollArea, QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, CardWidget, SubtitleLabel, TitleLabel

from src.services.AuthService import AuthService


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

        title_lbl = BodyLabel(title, self)
        value_lbl = TitleLabel(value, self)
        unit_lbl = BodyLabel(unit, self)
        unit_lbl.setStyleSheet("color: gray;")

        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
        layout.addWidget(unit_lbl)


class HomePage(QWidget):
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
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ─── Welcome header ───
        self._welcome_label = TitleLabel(f"Selamat datang, {username}!", content)
        desc = BodyLabel("Pantau jejak karbon harian kamu di sini.", content)
        desc.setStyleSheet("color: gray;")
        layout.addWidget(self._welcome_label)
        layout.addWidget(desc)

        # ─── Summary cards ───
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

        # ─── Recent activity section ───
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
