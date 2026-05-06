import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon, MSFluentWindow

from src.pages.example import ExamplePage


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.example_interface = ExamplePage(self)

        self.addSubInterface(
            self.example_interface, FluentIcon.HOME, "Example", FluentIcon.HOME_FILL
        )

        self.resize(1000, 650)
        self.setWindowTitle("Carbonly")
        self.setWindowIcon(QIcon(":/qfluentwidgets/images/logo.png"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
