# login_dialog.py
import os
import webbrowser
from PySide6.QtWidgets import (
    QDialog, QLineEdit, QPushButton, QFormLayout, QMessageBox
)
from signup_dialog import KakaoSignupDialog


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("로그인")
        self.resize(300, 150)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("로그인")
        login_btn.clicked.connect(self.handle_login)

        signup_btn = QPushButton("회원가입")
        signup_btn.clicked.connect(self.open_signup)

        layout = QFormLayout()
        layout.addRow("아이디:", self.username)
        layout.addRow("비밀번호:", self.password)
        layout.addRow(login_btn)
        layout.addRow(signup_btn)
        self.setLayout(layout)

    def handle_login(self):
        user = self.username.text().strip()
        pwd = self.password.text().strip()
        # TODO: 실제 인증 로직 필요 (DB 조회 등)
        if user == "admin" and pwd == "1234":
            self.accept()
        else:
            QMessageBox.warning(self, "로그인 실패", "아이디 또는 비밀번호가 올바르지 않습니다.")

    def open_signup(self):
        dlg = KakaoSignupDialog(self)
        if dlg.exec() == QDialog.Accepted:
            QMessageBox.information(self, "가입 완료", "카카오로 회원가입 및 자동 로그인되었습니다.")
            self.accept()