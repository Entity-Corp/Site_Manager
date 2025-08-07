# ui/login_dialog.py
from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QMessageBox

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("로그인")
        self.resize(300, 120)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("로그인")
        login_btn.clicked.connect(self.handle_login)

        layout = QFormLayout()
        layout.addRow("아이디:", self.username)
        layout.addRow("비밀번호:", self.password)
        layout.addRow(login_btn)
        self.setLayout(layout)

    def handle_login(self):
        user = self.username.text().strip()
        pwd = self.password.text().strip()
        # TODO: 실제 인증 로직으로 교체
        if user == "admin" and pwd == "1234":
            self.accept()
        else:
            QMessageBox.warning(self, "오류", "아이디 또는 비밀번호가 올바르지 않습니다.")