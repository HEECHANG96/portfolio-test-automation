from pytest_testrail.plugin import pytestrail
from pages.login_page import NaverLogin
from playwright.sync_api import expect


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
def test_naver_login_credentials_input(playwright_client):
    """
    로그인 화면에서 예시 아이디와 비밀번호의 입력값 검증
    """
    login_page = NaverLogin(playwright_client.page)

    user_id = "test_user"
    password = "test_pw"

    # 1. 로그인 페이지 이동
    login_page.go_to_login_page()

    # 2. 예시 계정 정보 입력
    login_page.enter_credentials(
        user_id=user_id,
        password=password,
    )

    # 3. 입력값 검증
    expect(login_page.id_input).to_have_value(user_id)
    expect(login_page.password_input).to_have_value(password)


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
# pytest tests/test_login.py \
#   --testrail \
#   --tr-url https://yourcompany.testrail.io \
#   --tr-email user@example.com \
#   --tr-password your_api_key_here \
#   --tr-testrun-project-id 123 \
#   --tr-testrun-suite-id 456 \
#   --tr-testrun-name local_Naver-v1.0.0-login_0916_1
