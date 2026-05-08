import os
import sys

from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication

from src.controllers.AuthController import AuthController
from src.models.User import User
from src.windows.MainWindow import MainWindow

if __name__ == "__main__":
    load_dotenv()

    User.create_table()
    if os.environ.get("CARBONLY_DEBUG") == "MinimalKasiSpesifikasiYangKonsistenMasMba":
        print("[WAIT] Seeding Demo User Data... ", end="")
        User.seed_demo_user()
        print("[SUCCESS]")

    app = QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()

    # Pastikan window sudah ter-layout dengan benar sebelum menampilkan dialog
    QApplication.processEvents()

    if AuthController.initialize():
        w.home_interface.refresh()
    else:
        w._start_login()

    app.exec()
