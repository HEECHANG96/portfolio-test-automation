from locator.naver.login import Login


class NaverBase:
    def __init__(self, page, base_url: str | None = None):
        self.page = page
        self.base_url = base_url or Login.URL

    def go_to_naver_page(self):
        """네이버 메인 페이지로 이동"""
        self.page.goto(self.base_url)
