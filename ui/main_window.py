# ui/main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QTreeWidget, QTreeWidgetItem,
    QStackedWidget, QSplitter, QWidget, QHBoxLayout
)

from ui.pages.page_a import PageA
from ui.pages.page_b import PageB

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("메인 프로그램")
        self.resize(800, 600)

        # 좌측 메뉴 트리
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        root = QTreeWidgetItem(self.tree, ["기능 목록"])
        item_a = QTreeWidgetItem(root, ["페이지 A"])
        item_b = QTreeWidgetItem(root, ["페이지 B"])
        root.setExpanded(True)

        # 우측 스택 위젯
        self.stack = QStackedWidget()
        self.stack.addWidget(PageA())
        self.stack.addWidget(PageB())

        # 트리 클릭 시 페이지 전환
        self.tree.currentItemChanged.connect(self.change_page)

        # 레이아웃 분할기
        splitter = QSplitter()
        splitter.addWidget(self.tree)
        splitter.addWidget(self.stack)
        splitter.setStretchFactor(1, 1)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(splitter)
        self.setCentralWidget(container)

        # 상태바
        self.statusBar().showMessage("Ready")

    def change_page(self, current, previous):
        text = current.text(0)
        if text == "페이지 A":
            self.stack.setCurrentIndex(0)
            self.statusBar().showMessage("페이지 A 선택됨")
        elif text == "페이지 B":
            self.stack.setCurrentIndex(1)
            self.statusBar().showMessage("페이지 B 선택됨")