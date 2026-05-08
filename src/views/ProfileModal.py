from typing import cast

from PyQt6 import QtCore
from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtWidgets import QFrame, QPushButton
from PyQt6.QtWidgets import QLineEdit as QLineEditBase
from qfluentwidgets import (
    FluentIcon,
    LineEdit,
    MessageBoxBase,
    PrimaryPushButton,
    StrongBodyLabel,
    SubtitleLabel,
)

from src.services.AuthService import AuthService


class ProfileModal(MessageBoxBase):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Profile")
        self._setup_close_button()
        self._setup_ui()
        self.widget.installEventFilter(self)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:  # noqa: N802
        if obj == self.widget and event.type() == QEvent.Type.Resize:
            self._close_btn.move(self.widget.width() - 36, 4)
        return cast(bool, super().eventFilter(obj, event))

    def _setup_close_button(self) -> None:
        self._close_btn = QPushButton("", self.widget)
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
        self._close_btn.move(self.widget.width() - 36, 4)

    def _setup_ui(self) -> None:
        user = AuthService.get_current_user()
        current_username = user.username or "" if user else ""

        # ─── Change username section ───
        self.viewLayout.addWidget(SubtitleLabel("Ganti Username", self))

        self.viewLayout.addWidget(StrongBodyLabel("Username Baru", self))
        self._username_input = LineEdit(self)
        self._username_input.setPlaceholderText(
            f"Username saat ini: {current_username}"
        )
        self._username_input.setFixedHeight(40)
        self._username_input.returnPressed.connect(self._on_update_username)
        self.viewLayout.addWidget(self._username_input)

        self._username_msg = StrongBodyLabel("", self)
        self._username_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._username_msg.setVisible(False)
        self.viewLayout.addWidget(self._username_msg)

        btn_username = PrimaryPushButton("Update Username", self)
        btn_username.setFixedHeight(40)
        btn_username.clicked.connect(self._on_update_username)
        self.viewLayout.addWidget(btn_username)

        # Separator
        sep = QFrame(self)
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: rgba(0, 0, 0, 0.08);")
        self.viewLayout.addWidget(sep)

        # ─── Change password section ───
        self.viewLayout.addWidget(SubtitleLabel("Ganti Password", self))

        self.viewLayout.addWidget(StrongBodyLabel("Password Saat Ini", self))
        self._cur_pass_input = LineEdit(self)
        self._cur_pass_input.setPlaceholderText("Masukkan password saat ini")
        self._cur_pass_input.setEchoMode(QLineEditBase.EchoMode.Password)
        self._cur_pass_input.setFixedHeight(40)
        self.viewLayout.addWidget(self._cur_pass_input)

        self.viewLayout.addWidget(StrongBodyLabel("Password Baru", self))
        self._new_pass_input = LineEdit(self)
        self._new_pass_input.setPlaceholderText("Minimal 6 karakter")
        self._new_pass_input.setEchoMode(QLineEditBase.EchoMode.Password)
        self._new_pass_input.setFixedHeight(40)
        self.viewLayout.addWidget(self._new_pass_input)

        self.viewLayout.addWidget(StrongBodyLabel("Konfirmasi Password Baru", self))
        self._confirm_pass_input = LineEdit(self)
        self._confirm_pass_input.setPlaceholderText("Ulangi password baru")
        self._confirm_pass_input.setEchoMode(QLineEditBase.EchoMode.Password)
        self._confirm_pass_input.setFixedHeight(40)
        self._confirm_pass_input.returnPressed.connect(self._on_update_password)
        self.viewLayout.addWidget(self._confirm_pass_input)

        self._password_msg = StrongBodyLabel("", self)
        self._password_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._password_msg.setVisible(False)
        self.viewLayout.addWidget(self._password_msg)

        btn_password = PrimaryPushButton("Update Password", self)
        btn_password.setFixedHeight(40)
        btn_password.clicked.connect(self._on_update_password)
        self.viewLayout.addWidget(btn_password)

        # Hide default dialog buttons
        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.buttonGroup.setFixedHeight(0)

        self.widget.setMinimumWidth(400)

    def _on_update_username(self) -> None:
        new_username = self._username_input.text().strip()
        if not new_username:
            self._set_msg(self._username_msg, "Username tidak boleh kosong", error=True)
            return
        success, message = AuthService.update_username(new_username)
        if success:
            self._username_input.clear()
            self._username_input.setPlaceholderText(
                f"Username saat ini: {new_username}"
            )
            self._set_msg(self._username_msg, message, error=False)
        else:
            self._set_msg(self._username_msg, message, error=True)

    def _on_update_password(self) -> None:
        current = self._cur_pass_input.text()
        new_pass = self._new_pass_input.text()
        confirm = self._confirm_pass_input.text()

        if not current or not new_pass or not confirm:
            self._set_msg(
                self._password_msg, "Semua field harus diisi", error=True
            )
            return
        if new_pass != confirm:
            self._set_msg(
                self._password_msg, "Password baru tidak cocok", error=True
            )
            return
        success, message = AuthService.update_password(current, new_pass)
        if success:
            self._cur_pass_input.clear()
            self._new_pass_input.clear()
            self._confirm_pass_input.clear()
            self._set_msg(self._password_msg, message, error=False)
        else:
            self._set_msg(self._password_msg, message, error=True)

    def _set_msg(
        self, label: StrongBodyLabel, message: str, *, error: bool
    ) -> None:
        label.setStyleSheet(f"color: {'red' if error else 'green'};")
        label.setText(message)
        label.setVisible(True)
