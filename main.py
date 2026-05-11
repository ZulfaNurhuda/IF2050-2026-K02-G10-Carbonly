import os
import sys

from PyQt6.QtCore import QEvent, QObject
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QDialog, QWidget
from qfluentwidgets import FluentIcon, MSFluentWindow

from src.models.User import User
from src.pages.Example import ExamplePage
from src.views.LoginModal import LoginModal
from src.models.TargetEmisi import TargetEmisi


class _OverlayResizeFilter(QObject):
    def __init__(self, overlay: QWidget, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._overlay = overlay

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:  # noqa: N802
        if event.type() == QEvent.Type.Resize:
            self._overlay.setGeometry(obj.rect())
        return False


class MainWindow(MSFluentWindow):
    def __init__(self) -> None:
        super().__init__()
        self.example_interface = ExamplePage(self)

        self.addSubInterface(
            self.example_interface, FluentIcon.HOME, "Example", FluentIcon.HOME_FILL
        )

        self.resize(1000, 650)
        self.setWindowTitle("Carbonly")
        self.setWindowIcon(QIcon(":/qfluentwidgets/images/logo.png"))


if __name__ == "__main__":
    User.create_table()
    TargetEmisi.create_table()
    if os.environ.get("CARBONLY_DEBUG") == "1":
        User.seed_demo_user()

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()

    overlay = QWidget(w)
    overlay.setGeometry(0, 0, w.width(), w.height())
    overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.4);")
    overlay.show()

    _resize_filter = _OverlayResizeFilter(overlay, w)
    w.installEventFilter(_resize_filter)

    login_modal = LoginModal(w)

    def on_login_finished() -> None:
        w.removeEventFilter(_resize_filter)
        overlay.close()
        overlay.deleteLater()

    login_modal.accepted.connect(on_login_finished)

    if login_modal.exec() != QDialog.DialogCode.Accepted:
        sys.exit(0)

    app.exec()
