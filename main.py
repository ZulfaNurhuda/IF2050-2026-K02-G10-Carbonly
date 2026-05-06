import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import MSFluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF

from src.pages.example import ExamplePage


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.example_interface = ExamplePage(self)

        self.addSubInterface(
            self.example_interface,
            FIF.HOME,
            'Example',
            FIF.HOME_FILL
        )

        self.resize(1000, 650)
        self.setWindowTitle('Carbonly')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()