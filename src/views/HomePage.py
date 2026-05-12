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
from src.pages.log_aktivitas import LogAktivitasPage
from src.views.RekapitulasiView import RekapitulasiView


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
        if self._rekap is not None:
            self._rekap.refresh()

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

        # Rekapitulasi
        self._rekap = RekapitulasiView(content)
        layout.addWidget(self._rekap)

        self._log_aktivitas = LogAktivitasPage(content)
        self._log_aktivitas.data_changed.connect(self._rekap.refresh)
        self._log_aktivitas._lblJudul.hide()
        self._log_aktivitas._lblSubjudul.hide()
        self._log_aktivitas.layout().setContentsMargins(0, 0, 0, 0)
        self._log_aktivitas._tabel.setMinimumHeight(300)

        log_header = QHBoxLayout()
        log_header.addWidget(SubtitleLabel("Aktivitas Terbaru", content))
        log_header.addStretch()
        log_header.addWidget(self._log_aktivitas._btnTambah)
        layout.addLayout(log_header)
        layout.addWidget(self._log_aktivitas)

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
