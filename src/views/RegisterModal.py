from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout
from qfluentwidgets import PrimaryPushButton, SubtitleLabel, StrongBodyLabel, FluentIcon as FIF


class RegisterModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register - Carbonly")
        self.setModal(True)
        self._setup_ui()

    def _setup_ui(self):
        title_label = SubtitleLabel("Create Account", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        username_label = StrongBodyLabel("Username", self)
        self._username_input = LineEdit(self)
        self._username_input.setPlaceholderText("Enter username (min 3 characters)")
        self._username_input.setFixedHeight(40)

        password_label = StrongBodyLabel("Password", self)
        self._password_input = LineEdit(self)
        self._password_input.setPlaceholderText("Enter password (min 6 characters)")
        self._password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._password_input.setFixedHeight(40)

        confirm_label = StrongBodyLabel("Confirm Password", self)
        self._confirm_input = LineEdit(self)
        self._confirm_input.setPlaceholderText("Confirm your password")
        self._confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._confirm_input.setFixedHeight(40)

        self._error_label = StrongBodyLabel("", self)
        self._error_label.setStyleSheet("color: red;")
        self._error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._error_label.setVisible(False)

        self._register_button = PrimaryPushButton("Register", self)
        self._register_button.setFixedHeight(40)
        self._register_button.clicked.connect(self._on_register_clicked)

        self._cancel_button = QPushButton("Cancel", self)
        self._cancel_button.setFixedHeight(40)
        self._cancel_button.clicked.connect(self.reject)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(32, 32, 32, 32)

        main_layout.addWidget(title_label)
        main_layout.addSpacing(8)
        main_layout.addWidget(username_label)
        main_layout.addWidget(self._username_input)
        main_layout.addWidget(password_label)
        main_layout.addWidget(self._password_input)
        main_layout.addWidget(confirm_label)
        main_layout.addWidget(self._confirm_input)
        main_layout.addWidget(self._error_label)
        main_layout.addWidget(self._register_button)
        main_layout.addWidget(self._cancel_button)

        self.setFixedSize(400, 480)

    def _on_register_clicked(self):
        from src.services.auth_service import register_user

        username = self._username_input.text().strip()
        password = self._password_input.text()
        confirm = self._confirm_input.text()

        if not username or not password or not confirm:
            self._show_error("Please fill in all fields")
            return

        if password != confirm:
            self._show_error("Passwords do not match")
            return

        success, message = register_user(username, password)
        if success:
            self.accept()
        else:
            self._show_error(message)

    def _show_error(self, message: str):
        self._error_label.setText(message)
        self._error_label.setVisible(True)


class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background: transparent;
            }
            QLineEdit:focus {
                border: 2px solid #0078D4;
            }
        """)