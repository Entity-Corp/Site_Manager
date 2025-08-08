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


# pip freeze > requirements.txt    현재 설치된 모듈 정보를 저장한다.
# 향후 가상환경에서 pip install -r requirements.txt 입력. requirements.txt 파일 안에 정리된 리스트의 모든 가상환경을 설치한다.