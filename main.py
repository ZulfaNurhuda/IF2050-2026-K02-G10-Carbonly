import ctypes
import os
import sys

from dotenv import load_dotenv
from PyQt6.QtCore import QtMsgType, qInstallMessageHandler
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

if sys.platform == "win32":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("carbonly.app")


def _qt_msg_handler(msg_type, context, msg):
    if "QFont::setPointSize" in msg:
        return
    if "wildcard call disconnects from destroyed signal of QPropertyAnimation" in msg:
        return
    if msg_type not in (QtMsgType.QtDebugMsg, QtMsgType.QtInfoMsg):
        print(f"[Qt] {msg}", file=sys.stderr)

from src.controllers.ActivityLogController import ActivityLogController
from src.controllers.AuthController import AuthController
from src.models.EmissionTarget import EmissionTarget
from src.models.User import User
from src.windows.MainWindow import MainWindow

if __name__ == "__main__":
    load_dotenv()

    User.create_table()
    EmissionTarget.create_table()
    ActivityLogController.initialize_database()

    if os.environ.get("CARBONLY_DEBUG") == "MinimalKasiSpesifikasiYangKonsistenMasMba":
        print("[WAIT] Seeding Demo User Data... ", end="")
        User.seed_demo_user()
        print("[SUCCESS]")

    qInstallMessageHandler(_qt_msg_handler)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("favicon.ico"))
    w = MainWindow()
    w.showMaximized()

    QApplication.processEvents()

    if AuthController.initialize():
        w.home_interface.refresh()
    else:
        w._start_login()

    app.exec()
