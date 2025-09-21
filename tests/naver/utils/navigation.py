from locator.naver.login import Login


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
