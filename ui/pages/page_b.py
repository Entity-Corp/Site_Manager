# ui/pages/page_b.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class PageB(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        label = QLabel("여기는 페이지 B")
        layout = QVBoxLayout(self)
        layout.addWidget(label)