import os
import sys

from PyQt6.QtCore import QEvent, QObject
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtWidgets import QApplication, QDialog, QWidget
from qfluentwidgets import Action, FluentIcon, MSFluentWindow, RoundMenu

from src.models.User import User
from src.pages.HomePage import HomePage
from src.services.AuthService import AuthService
from src.views.LoginModal import LoginModal
from src.views.ProfileModal import ProfileModal


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
        self.home_interface = HomePage(self)
        self.addSubInterface(
            self.home_interface, FluentIcon.HOME, "Beranda", FluentIcon.HOME_FILL
        )
        self.home_interface.profile_requested.connect(self._show_user_menu)
        self.resize(1100, 700)
        self.setWindowTitle("Carbonly")
        self.setWindowIcon(QIcon(":/qfluentwidgets/images/logo.png"))

    def _show_user_menu(self) -> None:
        menu = RoundMenu(parent=self)
        profile_action = Action(FluentIcon.PEOPLE, "Profile", menu)
        profile_action.triggered.connect(self._open_profile)
        menu.addAction(profile_action)
        menu.addSeparator()
        logout_action = Action(FluentIcon.POWER_BUTTON, "Logout", menu)
        logout_action.triggered.connect(self._logout)
        menu.addAction(logout_action)
        menu.exec(QCursor.pos(), ani=True)

    def _open_profile(self) -> None:
        ProfileModal(self).exec()
        self.home_interface.refresh()

    def _logout(self) -> None:
        AuthService.clear_session()
        _run_login(self)


def _run_login(window: MainWindow) -> None:
    overlay = QWidget(window)
    overlay.setGeometry(0, 0, window.width(), window.height())
    overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.4);")
    overlay.show()
    overlay.raise_()

    resize_filter = _OverlayResizeFilter(overlay, window)
    window.installEventFilter(resize_filter)

    login_modal = LoginModal(window)

    def on_accepted() -> None:
        AuthService.save_session()
        window.removeEventFilter(resize_filter)
        overlay.close()
        overlay.deleteLater()
        window.home_interface.refresh()

    login_modal.accepted.connect(on_accepted)

    if login_modal.exec() != QDialog.DialogCode.Accepted:
        sys.exit(0)


if __name__ == "__main__":
    User.create_table()
    if os.environ.get("CARBONLY_DEBUG") == "1":
        User.seed_demo_user()

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()

    if AuthService.load_session():
        w.home_interface.refresh()
    else:
        _run_login(w)

    app.exec()
