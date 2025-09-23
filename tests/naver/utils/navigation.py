from locator.naver.login import Login
from tests.naver.utils.base import NaverBase


class NaverNavigation(NaverBase):
    """
    네이버 네비게이션 유틸 클래스
    네이버 메인 메뉴 클릭 시 새 탭 열림 처리
    URL 검증 수행
    """

    def __init__(self, page, base_url: str | None = None):
        super().__init__(page, base_url)

    def click_and_wait(self, locator: dict, expected_url: str = None, timeout: int = 10000):
        """메뉴 클릭 후 새 탭이 열리고 URL 검증"""
        with self.page.context.expect_page() as new_page_info:
            self.page.locator(locator["value"]).click()
        new_tab = new_page_info.value

        # 새 탭 로딩 대기
        new_tab.wait_for_load_state("load", timeout=timeout)

        # URL 검증
        if expected_url:
            assert expected_url in new_tab.url, f"Expected '{expected_url}' in {new_tab.url}"

        return new_tab

    def is_correct_page(self, page, expected_url: str) -> bool:
        """URL 검증만 수행"""
        return expected_url in page.url
