from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QHBoxLayout, QPushButton
from PyQt6.QtWidgets import QLineEdit as QLineEditBase
from qfluentwidgets import (
    FluentIcon,
    HyperlinkLabel,
    LineEdit,
    MessageBoxBase,
    PrimaryPushButton,
    StrongBodyLabel,
)

from src.controllers.AuthController import AuthController


class LoginView(MessageBoxBase):
    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Login")
        self._is_register_mode: bool = False
        self._setup_close_button()
        self._setup_ui()
        self._connect_enter_key()

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

    def _setup_ui(self) -> None:
        self.username_label = StrongBodyLabel("Username", self)
        self._username_input = LineEdit(self)
        self._username_input.setPlaceholderText("Masukkan username")
        self._username_input.setFixedHeight(40)

        self.password_label = StrongBodyLabel("Password", self)
        self._password_input = LineEdit(self)
        self._password_input.setPlaceholderText("Masukkan password")
        self._password_input.setEchoMode(QLineEditBase.EchoMode.Password)
        self._password_input.setFixedHeight(40)

        self._confirm_label = StrongBodyLabel("Konfirmasi Password", self)
        self._confirm_label.setVisible(False)
        self._confirm_input = LineEdit(self)
        self._confirm_input.setPlaceholderText("Ulangi password baru")
        self._confirm_input.setEchoMode(QLineEditBase.EchoMode.Password)
        self._confirm_input.setFixedHeight(40)
        self._confirm_input.setVisible(False)

        self._msg_label = StrongBodyLabel("", self)
        self._msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._msg_label.setVisible(False)

        self._register_link = HyperlinkLabel("Belum punya akun? Daftar", self)
        self._register_link.clicked.connect(self._toggle_mode)

        self._submit_button = PrimaryPushButton("Login", self)
        self._submit_button.setFixedHeight(40)
        self._submit_button.clicked.connect(self._on_submit)

        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.buttonGroup.setFixedHeight(0)

        self.viewLayout.addWidget(self.username_label)
        self.viewLayout.addWidget(self._username_input)
        self.viewLayout.addWidget(self.password_label)
        self.viewLayout.addWidget(self._password_input)
        self.viewLayout.addWidget(self._confirm_label)
        self.viewLayout.addWidget(self._confirm_input)
        self.viewLayout.addWidget(self._msg_label)
        self.viewLayout.addWidget(self._submit_button)
        self.viewLayout.addWidget(self._register_link)

        self.widget.setMinimumWidth(360)

    def _connect_enter_key(self) -> None:
        self._username_input.returnPressed.connect(self._on_submit)
        self._password_input.returnPressed.connect(self._on_submit)
        self._confirm_input.returnPressed.connect(self._on_submit)

    def _toggle_mode(self) -> None:
        self._is_register_mode = not self._is_register_mode
        self._msg_label.setVisible(False)
        if self._is_register_mode:
            self.setWindowTitle("Daftar")
            self._submit_button.setText("Daftar")
            self._register_link.setText("Sudah punya akun? Login")
            self._confirm_label.setVisible(True)
            self._confirm_input.setVisible(True)
        else:
            self.setWindowTitle("Login")
            self._submit_button.setText("Login")
            self._register_link.setText("Belum punya akun? Daftar")
            self._confirm_label.setVisible(False)
            self._confirm_input.setVisible(False)

    def _on_submit(self) -> None:
        if self._is_register_mode:
            self._on_register()
        else:
            self._on_login()

    def _on_login(self) -> None:
        username = self._username_input.text().strip()
        password = self._password_input.text()
        success, message = AuthController.login(username, password)
        if success:
            self.accept()
        else:
            self._set_msg(self._msg_label, message, error=True)

    def _on_register(self) -> None:
        username = self._username_input.text().strip()
        password = self._password_input.text()
        confirm = self._confirm_input.text()
        success, message = AuthController.register(username, password, confirm)
        if success:
            self._set_msg(self._msg_label, message, error=False)
            self._toggle_mode()
        else:
            self._set_msg(self._msg_label, message, error=True)

    def _set_msg(self, label: StrongBodyLabel, message: str, *, error: bool) -> None:
        label.setStyleSheet(f"color: {'red' if error else 'green'};")
        label.setText(message)
        label.setVisible(True)
