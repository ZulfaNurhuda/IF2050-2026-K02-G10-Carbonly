import sys

from PyQt6.QtGui import QCursor, QIcon
from qfluentwidgets import Action, FluentIcon, MSFluentWindow, RoundMenu
from qfluentwidgets.components.widgets.menu import MenuAnimationType

from src.controllers.AuthController import AuthController
from src.views.HomePage import HomePage
from src.views.LoginView import LoginView
from src.views.ProfileView import ProfileView


class MainWindow(MSFluentWindow):
    def __init__(self) -> None:
        super().__init__()
        self.home_interface = HomePage(self)
        self.addSubInterface(
            self.home_interface, FluentIcon.HOME, "Beranda", FluentIcon.HOME_FILL
        )
        self.home_interface.profile_requested.connect(self._show_user_menu)
        self.setMinimumSize(1100, 700)
        self.setWindowTitle("Carbonly")
        self.setWindowIcon(QIcon(":/qfluentwidgets/images/logo.png"))

    def _start_login(self) -> None:
        login_view = LoginView(self)
        login_view.accepted.connect(self.home_interface.refresh)
        login_view.rejected.connect(lambda: sys.exit(0))
        login_view.open()
        self.titleBar.raise_()

    def _show_user_menu(self) -> None:
        menu = RoundMenu(parent=self)
        menu.view.setGraphicsEffect(None)
        menu.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        profile_action = Action(FluentIcon.PEOPLE, "Profile", menu)
        profile_action.triggered.connect(self._open_profile)
        menu.addAction(profile_action)

        menu.addSeparator()

        logout_action = Action(FluentIcon.POWER_BUTTON, "Logout", menu)
        logout_action.triggered.connect(self._logout)
        menu.addAction(logout_action)

        menu.exec(QCursor.pos(), aniType=MenuAnimationType.NONE)

    def _open_profile(self) -> None:
        profile_view = ProfileView(self)
        profile_view.finished.connect(lambda _: self.home_interface.refresh())
        profile_view.open()
        self.titleBar.raise_()

    def _logout(self) -> None:
        AuthController.logout()
        self._start_login()
