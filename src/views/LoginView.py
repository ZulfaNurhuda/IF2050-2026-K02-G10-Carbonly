from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QLineEdit as QLineEditBase
from qfluentwidgets import (
    HyperlinkLabel,
    LineEdit,
    MessageBoxBase,
    PrimaryPushButton,
    StrongBodyLabel,
)

from src.controllers.AuthController import AuthController


class LoginView(MessageBoxBase):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Login")
        self._is_register_mode: bool = False
        self._setup_ui()
        self._connect_enter_key()

    def _setup_ui(self) -> None:
        self.username_label = StrongBodyLabel("Username", self)
        self._username_input = LineEdit(self)
        self._username_input.setPlaceholderText("Enter username")
        self._username_input.setFixedHeight(40)

        self.password_label = StrongBodyLabel("Password", self)
        self._password_input = LineEdit(self)
        self._password_input.setPlaceholderText("Enter password")
        self._password_input.setEchoMode(QLineEditBase.EchoMode.Password)
        self._password_input.setFixedHeight(40)

        self._confirm_label = StrongBodyLabel("Confirm Password", self)
        self._confirm_label.setVisible(False)
        self._confirm_input = LineEdit(self)
        self._confirm_input.setPlaceholderText("Confirm your password")
        self._confirm_input.setEchoMode(QLineEditBase.EchoMode.Password)
        self._confirm_input.setFixedHeight(40)
        self._confirm_input.setVisible(False)

        self._error_label = StrongBodyLabel("", self)
        self._error_label.setStyleSheet("color: red;")
        self._error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._error_label.setVisible(False)

        self._register_link = HyperlinkLabel("Don't have an account? Register", self)
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
        self.viewLayout.addWidget(self._error_label)
        self.viewLayout.addWidget(self._submit_button)
        self.viewLayout.addWidget(self._register_link)

        self.widget.setMinimumWidth(360)

    def _connect_enter_key(self) -> None:
        self._username_input.returnPressed.connect(self._on_submit)
        self._password_input.returnPressed.connect(self._on_submit)
        self._confirm_input.returnPressed.connect(self._on_submit)

    def _toggle_mode(self) -> None:
        self._is_register_mode = not self._is_register_mode
        if self._is_register_mode:
            self.setWindowTitle("Register")
            self._submit_button.setText("Register")
            self._register_link.setText("Already have an account? Login")
            self._confirm_label.setVisible(True)
            self._confirm_input.setVisible(True)
            self._error_label.setVisible(False)
        else:
            self.setWindowTitle("Login")
            self._submit_button.setText("Login")
            self._register_link.setText("Don't have an account? Register")
            self._confirm_label.setVisible(False)
            self._confirm_input.setVisible(False)
            self._error_label.setVisible(False)

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
            self._show_error(message)

    def _on_register(self) -> None:
        username = self._username_input.text().strip()
        password = self._password_input.text()
        confirm = self._confirm_input.text()
        success, message = AuthController.register(username, password, confirm)
        if success:
            self._show_success(message)
            self._toggle_mode()
        else:
            self._show_error(message)

    def _show_error(self, message: str) -> None:
        self._error_label.setStyleSheet("color: red;")
        self._error_label.setText(message)
        self._error_label.setVisible(True)

    def _show_success(self, message: str) -> None:
        self._error_label.setStyleSheet("color: green;")
        self._error_label.setText(message)
        self._error_label.setVisible(True)
