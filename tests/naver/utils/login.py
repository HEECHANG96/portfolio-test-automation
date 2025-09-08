import time
from locator.naver.login import Login


class NaverLogin:
    """
    네이버 로그인 유틸 클래스
    실제 계정 없이 테스트 구조를 보여주는 예시
    """
    def __init__(self, page):
        self.page = page

    def go_to_login_page(self):
        # 메인 페이지로 이동
        self.page.goto(Login.URL)
        # 로그인 버튼 클릭 (메인 페이지)
        self.page.locator(Login.LOGIN_BTN_MAIN["value"]).click()
        time.sleep(3)

    def enter_credentials(self, user_id="test_user", password="test_pw"):
        # 입력창에 ID/PW 입력
        self.page.locator(Login.ID_INPUT["value"]).fill(user_id)
        self.page.locator(Login.PWD_INPUT["value"]).fill(password)

    def click_login(self):
        # 로그인 버튼 클릭
        # 실제 계정 로그인은 실행하지 않고 흐름만 보여줌
        self.page.locator(Login.LOGIN_BTN_FORM["value"]).click()
        pass

    def login_success(self):
        # 실제 로그인 확인은 생략, True 가정
        return True
