from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QDialog, QLineEdit as QLineEditBase, QVBoxLayout
from qfluentwidgets import LineEdit, StrongBodyLabel, HyperlinkLabel, MessageBoxBase


class LoginModal(MessageBoxBase):
    login_succeeded = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self._setup_ui()

    def _setup_ui(self):
        self.username_label = StrongBodyLabel("Username", self)
        self._username_input = LineEdit(self)
        self._username_input.setPlaceholderText("Enter username")
        self._username_input.setFixedHeight(40)

        self.password_label = StrongBodyLabel("Password", self)
        self._password_input = LineEdit(self)
        self._password_input.setPlaceholderText("Enter password")
        self._password_input.setEchoMode(QLineEditBase.EchoMode.Password)
        self._password_input.setFixedHeight(40)

        self._error_label = StrongBodyLabel("", self)
        self._error_label.setStyleSheet("color: red;")
        self._error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._error_label.setVisible(False)

        self._register_link = HyperlinkLabel("Don't have an account? Register", self)
        self._register_link.clicked.connect(self._on_register_clicked)

        self.yesButton.setText("Login")
        self.yesButton.clicked.connect(self._on_login_clicked)
        self.cancelButton.setText("Cancel")
        self.cancelButton.clicked.connect(self.reject)

        self.viewLayout.addWidget(self.username_label)
        self.viewLayout.addWidget(self._username_input)
        self.viewLayout.addWidget(self.password_label)
        self.viewLayout.addWidget(self._password_input)
        self.viewLayout.addWidget(self._error_label)
        self.viewLayout.addWidget(self._register_link)

        self.widget.setMinimumWidth(360)

    def _on_login_clicked(self):
        from src.services.auth_service import verify_user

        username = self._username_input.text().strip()
        password = self._password_input.text()

        if not username or not password:
            self._show_error("Please enter username and password")
            return

        if verify_user(username, password):
            self.login_succeeded.emit()
            self.accept()
        else:
            self._show_error("Invalid username or password")

    def _on_register_clicked(self):
        from src.views.RegisterModal import RegisterModal

        register_dialog = RegisterModal(self)
        if register_dialog.exec() == QDialog.DialogCode.Accepted:
            self._show_success("Registration successful! Please login.")

    def _show_error(self, message: str):
        self._error_label.setText(message)
        self._error_label.setVisible(True)

    def _show_success(self, message: str):
        self._error_label.setText(f"<span style='color: green;'>{message}</span>")
        self._error_label.setVisible(True)
