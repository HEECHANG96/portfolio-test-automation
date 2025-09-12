import pytest
from utils.login import NaverLogin


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