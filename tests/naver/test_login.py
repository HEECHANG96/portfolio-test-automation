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
