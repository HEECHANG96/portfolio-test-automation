from locator.login import Login
from locator.search import Search

class NaverNavigation:
    """
    네이버 네비게이션 유틸 클래스
    네이버 메인 메뉴 클릭 시 새 탭 열림 처리
    URL 검증 수행
    """

    def __init__(self, page):
        self.page = page

    def go_to_naver_page(self):
        self.page.goto(Login.URL)

    def click_and_wait(self, locator: dict, expected_url: str = None, timeout: int = 10000):
        # 메뉴 클릭 후 새 탭이 열리는 경우 감지
        with self.page.context.expect_page() as new_page_info:
            self.page.locator(locator["value"]).click()
        new_tab = new_page_info.value

        # 새 탭 페이지가 완전히 로드될 때까지 대기
        new_tab.wait_for_load_state("load", timeout=timeout)

        # URL이 예상값과 일치하면 검증
        if expected_url:
            assert expected_url in new_tab.url

        # 새 탭 객체 반환
        return new_tab

    def is_correct_page(self, page, expected_url: str) -> bool:
        """URL 검증 수행"""
        return expected_url in page.url

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
        # Playwright에서 페이지가 완전히 로드될 때까지 기다리는 기능을 수행
        # 브라우저에서 페이지의 **로드 상태(load state)**를 관찰하고, 특정 상태가 될 때까지 대기(blocking) 함
        # 검색 후 결과 페이지가 완전히 준비될 때까지 기다리는 안전장치 역할
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        return self.page.url

    def is_result_page(self):
        """
        검색 결과 페이지 여부 확인
        """
        current_url = self.page.url
        return "search.naver.com" in current_url