from locator.naver.login import Login
from locator.naver.search import Search


class NaverSearch:
    """
    네이버 검색 유틸 클래스
    검색창 및 검색 버튼 관련 동작을 처리
    """
    def __init__(self, page):
        self.page = page

    def go_to_naver_page(self):
        # 메인 페이지 이동
        self.page.goto(Login.URL)

    def search_bar_visible(self):
        """
        검색 입력창이 노출되는지 확인
        """
        return self.page.is_visible(Search.SEARCH_BAR["value"])

    def search_button_visible(self):
        """
        검색 버튼이 노출되는지 확인
        """
        return self.page.is_visible(Search.SEARCH_BTN["value"])

    def enter_keyword(self, keyword: str):
        """
        검색어 입력
        """
        self.page.locator(Search.SEARCH_BAR["value"]).fill(keyword)

    def click_search_button(self):
        """
        검색 버튼 클릭
        """
        self.page.locator(Search.SEARCH_BTN["value"]).click()

    def search_and_wait_redirect(self, keyword: str, timeout: int = 5000):
        """
        검색어 입력 후 검색 버튼 클릭 → 결과 페이지 이동까지 확인
        """
        self.enter_keyword(keyword)
        self.click_search_button()
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        return self.page.url

    def is_result_page(self):
        """
        검색 결과 페이지 여부 확인
        """
        current_url = self.page.url
        return "search.naver.com" in current_url
