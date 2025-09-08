from playwright.sync_api import sync_playwright


class PlaywrightClient:
    def __init__(self, headless=True, browser_type="chromium", width=1920, height=1080):
        self.headless = headless
        self.browser_type = browser_type
        self.width = width
        self.height = height
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    # 브라우저를 실제로 시작하는 메서드
    def start_browser(self):
        # Playwright 프로세스를 시작하고, 제어 핸들을 self.playwright에 저장
        self.playwright = sync_playwright().start()

        # self.browser_type 문자열("chromium"/"firefox"/"webkit")에 맞는 런처 객체를 동적으로 얻는다.
        # 예: self.playwright.chromium / self.playwright.firefox / self.playwright.webkit
        browser_launcher = getattr(self.playwright, self.browser_type)

        # 해당 엔진으로 브라우저 실행. headless 인자에 따라 창 표시 여부 결정
        # (참고: 여기서 'chromium'은 크롬이 아닌 Playwright가 번들한 Chromium임.
        #  실제 Chrome을 쓰려면 channel="chrome"을 추가해야 함)
        self.browser = browser_launcher.launch(headless=self.headless)

        # 새 브라우저 컨텍스트 생성. viewport로 페이지 뷰포트 크기를 설정
        # (컨텍스트는 쿠키/세션이 분리되는 독립적인 브라우저 프로필 같은 것)
        self.context = self.browser.new_context(
            viewport={"width": self.width, "height": self.height}
        )

        # 위 컨텍스트에서 새 탭(Page) 하나를 연다. 이후 상호작용은 보통 self.page로 진행
        self.page = self.context.new_page()

    # 리소스를 정리(닫기)하는 메서드
    def stop(self):
        if self.context:
            self.context.close()

        # 브라우저 프로세스 종료
        if self.browser:
            self.browser.close()

        # Playwright 드라이버 자체 종료(백그라운드 프로세스/서버 정리)
        if self.playwright:
            self.playwright.stop()
