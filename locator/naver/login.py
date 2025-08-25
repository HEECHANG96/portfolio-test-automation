class Login:
    URL = "https://www.naver.com/"

    # 메인 페이지 로그인 버튼
    LOGIN_BTN_MAIN = {"type": "XPATH", "value": '//a[contains(@class, "MyView-module__link_login") and contains(text(), "로그인")]'}

    # 로그인 화면 입력창
    ID_INPUT = {"type": "XPATH", "value": '//input[@id="id"]'}
    PWD_INPUT = {"type": "XPATH", "value": '//input[@id="pw"]'}

    # 로그인 화면 로그인 버튼
    LOGIN_BTN_FORM = {"type": "XPATH", "value": '//button[@id="log.login"]'}

    # 로그아웃 버튼
    LOGOUT_BTN = {"type": "XPATH", "value": '//button[contains(@class, "btn_logout") and text()="로그아웃"]'}