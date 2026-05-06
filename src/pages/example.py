from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import SubtitleLabel, setFont


class ExamplePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('example-page')

        lbl = SubtitleLabel('Example Page', self)
        setFont(lbl, 20)
        lbl.setAlignment(Qt.AlignCenter)

        QHBoxLayout(self).addWidget(lbl, 1, Qt.AlignCenter)