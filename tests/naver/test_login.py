import pytest
from pytest_testrail.plugin import pytestrail
from utils.login import NaverLogin


@pytestrail.case('C10001')
def test_main_login_button_visible(playwright_client):
    """
    메인 페이지 로그인 버튼 UI 확인
    - 메인 화면에 로그인 버튼이 노출되는지 확인
    """
    client = playwright_client
    login_util = NaverLogin(client.page)

    # 1. 메인 페이지 이동
    login_util.go_to_naver_page()

    # 2. 메인 로그인 버튼 존재 여부 확인
    assert login_util.main_login_button_visible(), "메인 페이지에 로그인 버튼이 노출되어야 함"


@pytestrail.case('C10002')
def test_form_login_button_visible(playwright_client):
    """
    로그인 화면 로그인 버튼 UI 확인
    - 로그인 화면에 로그인 버튼이 노출되는지 확인
    """
    client = playwright_client
    login_util = NaverLogin(client.page)

    # 1. 로그인 페이지 이동
    login_util.go_to_login_page()

    # 2. 로그인 화면 버튼 존재 여부 확인
    assert login_util.form_login_button_visible(), "로그인 화면에 로그인 버튼이 노출되어야 함"


@pytestrail.case('C10003')
def test_naver_login(playwright_client):
    """
    네이버 로그인 흐름
    - 실제 계정 없이 진행
    """
    client = playwright_client
    login_util = NaverLogin(client.page)

    # 1. 로그인 페이지 이동
    login_util.go_to_login_page()

    # 2. ID/PW 입력
    login_util.enter_credentials()

    # 3. 로그인 버튼 클릭 (실제 실행 X)
    login_util.click_login()

    # 4. 로그인 성공 여부 확인 (Mock)
    assert login_util.login_success(), "로그인 흐름 시연 성공"


@pytestrail.case('C10004')
def test_naver_login_invalid_credentials(playwright_client):
    """
    네이버 로그인 실패 흐름 (잘못된 아이디/비밀번호)
    - 실제 인증은 생략하고 입력/흐름만 확인
    """
    client = playwright_client
    login_util = NaverLogin(client.page)

    # 1. 로그인 페이지 이동
    login_util.go_to_login_page()

    # 2. 잘못된 ID/PW 입력
    login_util.enter_credentials(user_id="wrong_user", password="wrong_pw")

    # 3. 로그인 버튼 클릭
    login_util.click_login_btn()

    # 4. 에러 메시지 노출 확인
    assert login_util.login_fail_visible()


@pytestrail.case('C10005')
def test_naver_login_empty_credentials(playwright_client):
    """
    네이버 로그인 실패 흐름 (아이디/비밀번호 미입력)
    - 로그인 버튼이 비활성화 상태인지 확인
    """
    client = playwright_client
    login_util = NaverLogin(client.page)

    # 1. 로그인 페이지 이동
    login_util.go_to_login_page()

    # 2. 아이디/비밀번호를 입력하지 않음
    login_util.enter_credentials(user_id="", password="")

    # 3. 로그인 버튼 비활성화 여부 확인
    assert login_util.is_login_button_disabled(), "아이디/비밀번호 미입력 시 로그인 버튼은 비활성화 상태여야 함"


# TestRail 실행 명령어 예시
# pytest tests/ \
#   --testrail \
#   --tr-url https://yourcompany.testrail.io \
#   --tr-email user@example.com \
#   --tr-password your_api_key_here \
#   --tr-project-id 1 \
#   --tr-suite-id 101