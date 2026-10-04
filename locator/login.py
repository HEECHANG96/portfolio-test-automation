class Login:
    URL = "https://www.naver.com/"

    # 메인 페이지 로그인 버튼
    LOGIN_BTN_MAIN = {
        "type": "XPATH",
        "value": '//a[contains(@class, "MyView-module__link_login") and contains(text(), "로그인")]'
    }

    # 로그인 화면 입력창
    ID_INPUT = {"type": "XPATH", "value": '//input[@id="id"]'}
    PWD_INPUT = {"type": "XPATH", "value": '//input[@id="pw"]'}

    # 로그인 실패 에러 메시지
    ERROR_MSG = {
        "type": "XPATH",
        "value": (
            '//div[@role="alert" '
            'and @data-case="메시지 == 비밀번호오류메시지"]'
        ),
    }

    # 로그인 화면 로그인 버튼
    LOGIN_BTN_FORM = {"type": "XPATH", "value": '//button[@id="loginBtn_row"]'}

    # 아이디 미입력 안내 메시지
    ID_REQUIRED_MESSAGE = "아이디 또는 전화번호를 입력해 주세요."

    # 로그아웃 버튼
    LOGOUT_BTN = {"type": "XPATH", "value": '//button[contains(@class, "btn_logout") and text()="로그아웃"]'}
