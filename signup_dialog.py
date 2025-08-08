# signup_dialog.py
from dotenv import load_dotenv
import os
load_dotenv()  # .env 파일의 키/값을 os.environ에 로드

client_id = os.getenv("KAKAO_REST_API_KEY")
rest_api_key = os.getenv("KAKAO_REST_API_KEY")
redirect_uri = os.getenv("KAKAO_REDIRECT_URI")
client_secret = os.getenv("KAKAO_CLIENT_SECRET")

import requests


from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QDialog, QVBoxLayout, QMessageBox
from PySide6.QtWebEngineWidgets import QWebEngineView

from sqlalchemy.exc import IntegrityError
from db_config import init_db, SessionLocal, User

# DB 초기화 (최초 1회만 호출해도 충분합니다)
init_db()


class KakaoSignupDialog(QDialog):
    """
    카카오 OAuth를 통해 회원가입 및 로그인 처리를 수행하는 다이얼로그.
    내장 WebView로 인가 코드를 가로채고, 토큰/유저 정보를 조회한 뒤 DB에 저장합니다.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("카카오 회원가입")
        self.resize(600, 800)

        # 환경 변수에서 REST API 키와 리다이렉트 URI 로드
        self.client_id = os.getenv("KAKAO_REST_API_KEY")
        self.rest_api_key  = os.getenv("KAKAO_REST_API_KEY")
        self.redirect_uri = os.getenv("KAKAO_REDIRECT_URI")
        self.client_secret = os.getenv("KAKAO_CLIENT_SECRET")
        print("client_id>>",self.client_id)# = os.getenv("KAKAO_REST_API_KEY")
        print("rest_api_key>>",self.rest_api_key)# = os.getenv("KAKAO_REST_API_KEY")
        print("redirect_uri>>",self.redirect_uri)# = os.getenv("KAKAO_REDIRECT_URI")
        print("client_secret>>",self.client_secret)# = os.getenv("KAKAO_REDIRECT_URI")


        if not self.client_id or not self.redirect_uri:
            QMessageBox.critical(
                self,
                "설정 오류",
                "환경 변수를 확인하세요:\n"
                "KAKAO_REST_API_KEY, KAKAO_REDIRECT_URI"
            )
            self.reject()
            return

        # 카카오 인가 URL 생성
        oauth_url = (
            "https://kauth.kakao.com/oauth/authorize"
            f"?response_type=code&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
        )

        print(oauth_url)

        # WebEngineView에 인가 페이지 로드
        self.webview = QWebEngineView(self)
        self.webview.load(QUrl(oauth_url))
        self.webview.urlChanged.connect(self._on_url_changed)

        layout = QVBoxLayout(self)
        layout.addWidget(self.webview)

    def _on_url_changed(self, url: QUrl):
        """
        redirect_uri로 리다이렉트된 URL을 가로채 인가 코드를 추출합니다.
        """
        url_str = url.toString()
        if not url_str.startswith(self.redirect_uri):
            return

        # URL에서 쿼리 파라미터 파싱
        query_items = dict(item.split('=', 1) for item in url.query().split('&') if '=' in item)
        code = query_items.get("code")
        print("code:::", code)
        if not code:
            QMessageBox.warning(self, "인증 실패", "인가 코드가 전달되지 않았습니다.")
            self.reject()
            return

        # 토큰 발급 → 사용자 정보 조회 → DB 저장
        access_token = self._request_token(code)
        print("Access Token:::", access_token)
        if not access_token:
            QMessageBox.warning(self, "토큰 발급 실패", "Access Token을 발급받지 못했습니다.")
            self.reject()
            return

        user_info = self._request_user_info(access_token)
        if not user_info:
            QMessageBox.warning(self, "정보 조회 실패", "카카오 사용자 정보를 가져오지 못했습니다.")
            self.reject()
            return

        saved = self._save_to_db(user_info)
        if saved:
            QMessageBox.information(self, "가입 완료", "카카오 회원가입이 완료되었습니다.")
        else:
            QMessageBox.information(self, "로그인 처리", "기존 사용자로 처리되었습니다.")
        self.accept()

    def _request_token(self, code: str) -> str | None:
        """
        인가 코드로 Access Token을 요청합니다.
        """
        token_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "client_secret": self.client_secret,
            "code": code
        }
        try:

            resp = requests.post(token_url, data=data)
            print("resp::",resp.text)
            print(resp.raise_for_status())
            resp.raise_for_status()
            r = resp.json().get("access_token")
            return r
        except Exception as e:
            print("토큰 요청 에러:", e)
            return None

    def _request_user_info(self, token: str) -> dict | None:
        print("token===", token)
        """
        Access Token으로 카카오 사용자 정보를 조회합니다.
        """
        profile_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            resp = requests.get(profile_url, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print("사용자 정보 조회 에러:", e)
            return None

    def _save_to_db(self, info: dict) -> bool:
        """
        SQLAlchemy를 통해 social_id 기준 신규 유저 등록을 시도합니다.
        중복 시 False를 반환하여 기존 로그인 처리로 넘어갑니다.
        """
        session = SessionLocal()
        try:
            kakao_id = str(info.get("id"))
            props = info.get("properties", {})
            account = info.get("kakao_account", {})

            user = User(
                social_id=kakao_id,
                nickname=props.get("nickname"),
                email=account.get("email")
            )
            session.add(user)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False
        except Exception as e:
            print("DB 저장 에러:", e)
            session.rollback()
            return False
        finally:
            session.close()