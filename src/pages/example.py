from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QWidget
from qfluentwidgets import SubtitleLabel, setFont


class ExamplePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("example-page")

        lbl = SubtitleLabel("Example Page", self)
        setFont(lbl, 20)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        QHBoxLayout(self).addWidget(lbl, 1, Qt.AlignmentFlag.AlignCenter)
