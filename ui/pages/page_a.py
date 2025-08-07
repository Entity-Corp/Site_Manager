# ui/pages/page_a.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class PageA(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        label = QLabel("여기는 페이지 A")
        layout = QVBoxLayout(self)
        layout.addWidget(label)