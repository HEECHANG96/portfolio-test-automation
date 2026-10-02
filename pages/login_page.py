import time
from playwright.sync_api import expect
from locator.login import Login


class NaverLogin:
    """
    네이버 로그인 유틸 클래스
    실제 계정 없이 테스트 구조를 보여주는 예시
    """
    def __init__(self, page):
        self.page = page
        self.id_input = page.locator(Login.ID_INPUT["value"])
        self.password_input = page.locator(Login.PWD_INPUT["value"])

    def go_to_naver_page(self):
        # 메인 페이지로 이동
        self.page.goto(Login.URL)

    def go_to_login_page(self):
        # 메인 페이지로 이동
        self.page.goto(Login.URL)
        # 로그인 버튼 클릭 (메인 페이지)
        self.page.locator(Login.LOGIN_BTN_MAIN["value"]).click()
        time.sleep(3)

    def main_login_button_visible(self):
        return self.page.is_visible(Login.LOGIN_BTN_MAIN["value"])

    def enter_credentials(self, user_id="test_user", password="test_pw"):
        self.id_input.fill(user_id)
        self.password_input.fill(password)

    def form_login_button_visible(self):
        return self.page.is_visible(Login.LOGIN_BTN_FORM["value"])

    def click_login_btn(self):
        # 로그인 버튼 클릭
        self.page.locator(Login.LOGIN_BTN_FORM["value"]).click()

    def login_fail_visible(self):
        """
        잘못된 아이디/비밀번호 입력 시 오류 메시지가 보이는지 확인
        """
        error_locator = self.page.locator(Login.ERROR_MSG["value"])
        # 최대 5초 동안 visible 될 때까지 기다림
        expect(error_locator).to_be_visible(timeout=5000)
        return error_locator.is_visible()

    def is_login_button_disabled(self):
        button_class = self.page.get_attribute(Login.LOGIN_BTN_FORM["value"], "class")
        return "off" in button_class if button_class else False
