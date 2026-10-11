from pytest_testrail.plugin import pytestrail
from pages.search_page import NaverSearch

SEARCH_KEYWORD = "테스트"


@pytestrail.case("C20001")
def test_search_input_visible(playwright_client):
    """
    네이버 메인 페이지의 검색 입력창 노출 확인
    """
    search_page = NaverSearch(playwright_client.page)

    # 1. 네이버 메인 페이지 이동
    search_page.go_to_naver_page()

    # 2. 검색 입력창 노출 확인
    assert search_page.search_bar_visible(), (
        "검색 입력창이 보이지 않음"
    )


@pytestrail.case("C20002")
def test_search_functionality_redirect(playwright_client):
    """
    검색어 입력 후 Enter 키로 결과 페이지 이동 확인
    """
    search_page = NaverSearch(playwright_client.page)

    # 1. 네이버 메인 페이지 이동
    search_page.go_to_naver_page()

    # 2. 검색어 입력 후 Enter 키 입력
    current_url = search_page.search_and_wait_redirect(
        SEARCH_KEYWORD
    )

    # 3. 검색 결과 페이지 이동 확인
    assert search_page.is_result_page(), (
        f"검색 결과 페이지로 이동하지 않음: {current_url}"
    )
