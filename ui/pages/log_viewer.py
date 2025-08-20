import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QTextEdit, QFileDialog, QPushButton,
    QHBoxLayout, QLineEdit, QToolBar, QMessageBox
)
from PySide6.QtCore import QTimer, Qt, QSettings
from PySide6.QtGui import QColor, QTextCharFormat, QIcon, QPalette, QTextCursor

LOG_LEVEL_COLORS = {
    "ERROR": QColor("red"),
    "WARNING": QColor("orange"),
    "INFO": QColor("green"),
    "DEBUG": QColor("gray")
}

class LogViewerTab(QWidget):
    def __init__(self, filepath, auto_scroll=True, filter_keyword=""):
        super().__init__()
        self.filepath = filepath
        self.last_size = 0
        self.modified = False
        self.auto_scroll = auto_scroll
        self.filter_keyword = filter_keyword

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_update)
        self.timer.start(1000)

        self.load_initial()

    def load_initial(self):
        try:
            self.last_size = os.path.getsize(self.filepath)
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                for line in lines:
                    self.append_line(line)
        except Exception as e:
            QMessageBox.warning(self, "파일 오류", f"파일을 읽을 수 없습니다:\n{e}")

    def check_update(self):
        try:
            current_size = os.path.getsize(self.filepath)
            if current_size > self.last_size:
                with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    f.seek(self.last_size)
                    new_lines = f.readlines()
                    for line in new_lines:
                        self.append_line(line)
                self.last_size = current_size
                self.modified = True
        except Exception as e:
            print(f"Error reading file: {e}")

    def append_line(self, line):
        if self.filter_keyword and self.filter_keyword not in line:
            return

        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        fmt = QTextCharFormat()

        for level, color in LOG_LEVEL_COLORS.items():
            if level in line:
                fmt.setForeground(color)
                break

        cursor.insertText(line, fmt)
        if self.auto_scroll:
            self.text_edit.moveCursor(QTextCursor.End)

class LogViewerMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log Viewer Pro")
        self.resize(1000, 700)
        self.setWindowIcon(QIcon("icon.png"))  # 아이콘 파일 경로

        self.settings = QSettings("JinoSoft", "LogViewerPro")

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("필터 키워드 입력")
        self.filter_input.textChanged.connect(self.apply_filter)

        self.open_button = QPushButton("로그 열기")
        self.open_button.setIcon(QIcon("open.png"))
        self.open_button.clicked.connect(self.open_file)

        self.scroll_toggle = QPushButton()
        self.scroll_toggle.setCheckable(True)
        self.scroll_toggle.setChecked(self.settings.value("auto_scroll", True, type=bool))
        self.update_scroll_button()
        self.scroll_toggle.clicked.connect(self.toggle_scroll)

        self.dark_mode_button = QPushButton("🌙 다크 모드")
        self.dark_mode_button.setCheckable(True)
        self.dark_mode_button.setChecked(self.settings.value("dark_mode", False, type=bool))
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(self.open_button)
        toolbar_layout.addWidget(self.scroll_toggle)
        toolbar_layout.addWidget(self.dark_mode_button)
        toolbar_layout.addWidget(self.filter_input)

        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar_layout)
        self.addToolBar(Qt.TopToolBarArea, self.create_toolbar(toolbar_widget))

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_tab_titles)
        self.timer.start(1000)

        if self.dark_mode_button.isChecked():
            self.enable_dark_mode()

    def create_toolbar(self, widget):
        toolbar = QToolBar()
        toolbar.addWidget(widget)
        return toolbar

    def open_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "로그 파일 선택")
        if filepath:
            tab = LogViewerTab(
                filepath,
                auto_scroll=self.scroll_toggle.isChecked(),
                filter_keyword=self.filter_input.text()
            )
            index = self.tabs.addTab(tab, os.path.basename(filepath))
            self.tabs.setCurrentIndex(index)

    def toggle_scroll(self):
        self.update_scroll_button()
        self.settings.setValue("auto_scroll", self.scroll_toggle.isChecked())
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            tab.auto_scroll = self.scroll_toggle.isChecked()

    def update_scroll_button(self):
        state = self.scroll_toggle.isChecked()
        self.scroll_toggle.setText("자동 스크롤 ON" if state else "자동 스크롤 OFF")

    def apply_filter(self):
        keyword = self.filter_input.text()
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            tab.filter_keyword = keyword
            tab.text_edit.clear()
            tab.load_initial()

    def update_tab_titles(self):
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            title = os.path.basename(tab.filepath)
            if tab.modified:
                self.tabs.setTabText(i, f"* {title}")
            else:
                self.tabs.setTabText(i, title)
            tab.modified = False

    def toggle_dark_mode(self):
        enabled = self.dark_mode_button.isChecked()
        self.settings.setValue("dark_mode", enabled)
        if enabled:
            self.enable_dark_mode()
        else:
            self.disable_dark_mode()

    def enable_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2b2b2b"))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor("#3c3f41"))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor("#3c3f41"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(palette)

    def disable_dark_mode(self):
        self.setPalette(QApplication.style().standardPalette())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = LogViewerMain()
    viewer.show()
    sys.exit(app.exec())