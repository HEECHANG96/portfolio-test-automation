
from locator.login import Login
from locator.search import Search


class NaverSearch:
    """
    네이버 검색 관련 동작을 처리하는 Page Object
    """

    def __init__(self, page):
        self.page = page

    def go_to_naver_page(self):
        """네이버 메인 페이지 이동"""
        self.page.goto(Login.URL)

    def search_bar_visible(self):
        """검색 입력창 노출 여부 확인"""
        return self.page.is_visible(Search.SEARCH_BAR["value"])

    def enter_keyword(self, keyword: str):
        """검색어 입력"""
        self.page.locator(Search.SEARCH_BAR["value"]).fill(keyword)

    def press_enter(self):
        """검색 입력창에서 Enter 키 입력"""
        self.page.locator(Search.SEARCH_BAR["value"]).press("Enter")

    def search_and_wait_redirect(self, keyword: str, timeout: int = 10000):
        """검색어 입력 후 검색 결과 페이지 이동 확인"""
        self.enter_keyword(keyword)
        self.press_enter()

        self.page.wait_for_url(
            "https://search.naver.com/**",
            wait_until="domcontentloaded",
            timeout=timeout
        )

        return self.page.url

    def is_result_page(self):
        """검색 결과 페이지 여부 확인"""
        return self.page.url.startswith("https://search.naver.com/")
