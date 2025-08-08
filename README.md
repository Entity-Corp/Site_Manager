# 프로젝트의 시작
## 1. 목적
- 파이썬 ui 프로그램의 기본 틀 작성


## 🔐로그인


## 2. 카카오 OAuth 회원가입 흐름

1.  사용자가 회원가입 버튼 클릭 → KakaoSignupDialog 실행
2.  다이얼로그 내에서 카카오 OAuth 인가 URL 열기
  ⁠◦  URL 형식:
https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}
3.  사용자가 카카오 로그인 A·동의 후 리다이렉트 → redirect_uri로 code 수신
4.  서버(또는 클라이언트)에서 토큰 요청
  ⁠◦  POST https://kauth.kakao.com/oauth/token
  ⁠◦  파라미터: grant_type=authorization_code, client_id, redirect_uri, code A
5.  발급받은 access_token으로 사용자 정보 조회
  ⁠◦  GET https://kapi.kakao.com/v1/user/me
  ⁠◦  헤더: Authorization: Bearer {access_token} A
6.  반환된 id(social_id), kakao_account 내 프로필·이메일 등을 DB에 저장
7.  가입 또는 기존 사용자 판단 후 로그인 처리


