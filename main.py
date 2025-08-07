# main.py
import sys
from PySide6.QtWidgets import QApplication
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login = LoginDialog()
    if login.exec() == LoginDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)