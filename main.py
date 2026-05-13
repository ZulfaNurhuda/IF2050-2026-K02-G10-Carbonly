import os
import sys

from dotenv import load_dotenv
from PyQt6.QtCore import QtMsgType, qInstallMessageHandler
from PyQt6.QtWidgets import QApplication


def _qt_msg_handler(msg_type, context, msg):
    # qfluentwidgets sets app font with pixel size; Qt's rendering pipeline
    # internally calls setPointSize(-1) on these fonts — harmless, suppress it.
    if "QFont::setPointSize" in msg:
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
    w = MainWindow()
    w.showMaximized()

    QApplication.processEvents()

    if AuthController.initialize():
        w.home_interface.refresh()
    else:
        w._start_login()

    app.exec()
