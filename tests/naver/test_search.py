from pytest_testrail.plugin import pytestrail
from tests.naver.utils.search import NaverSearch

SEARCH_KEYWORD = "테스트"


@pytestrail.case('C20001')
def test_search_input_and_button_visible(playwright_client):
    """
    (UI) 검색 입력창과 검색 버튼 존재 확인
    """
    client = playwright_client
    search_util = NaverSearch(client.page)

    # 1. 네이버 페이지 이동
    search_util.go_to_naver_page()

    # 2. 검색 입력창 확인
    assert search_util.search_bar_visible(), "검색 입력창이 보이지 않음"

    # 3. 검색 버튼 확인
    assert search_util.search_button_visible(), "검색 버튼이 보이지 않음"


@pytestrail.case('C20002')
def test_search_functionality_redirect(playwright_client):
    """
    정상 검색 → 결과 페이지 이동 확인
    """
    client = playwright_client
    search_util = NaverSearch(client.page)

    # 1. 네이버 페이지 이동
    search_util.go_to_naver_page()

    # 2. 검색 실행 후 페이지 이동 확인
    current_url = search_util.search_and_wait_redirect(SEARCH_KEYWORD)

    assert search_util.is_result_page(), f"검색 결과 페이지로 이동하지 않음: {current_url}"
