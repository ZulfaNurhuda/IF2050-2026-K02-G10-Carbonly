import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon, MSFluentWindow

from src.pages.example import ExamplePage
from src.pages.log_aktivitas import LogAktivitasPage


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()

        # Halaman contoh
        self.example_interface = ExamplePage(self)
        self.addSubInterface(
            self.example_interface, FluentIcon.HOME, "Example", FluentIcon.HOME_FILL
        )

        # Halaman Log Aktivitas — tombol "Tambah Log" ada di dalam halaman ini
        self.log_aktivitas_interface = LogAktivitasPage(self)
        self.addSubInterface(
            self.log_aktivitas_interface, FluentIcon.CALORIES, "Log Aktivitas"
        )

        self.resize(1100, 680)
        self.setWindowTitle("Carbonly")
        self.setWindowIcon(QIcon(":/qfluentwidgets/images/logo.png"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
