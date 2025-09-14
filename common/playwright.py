from typing import Optional, Tuple
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page


class PlaywrightClient:
    def __init__(
        self,
        browser_type: str = "chromium",            # "chromium", "firefox", "webkit"
        headless: bool = True,                     # 브라우저 UI 표시 여부
        viewport: Tuple[int, int] = (1920, 1080),  # 뷰포트 크기
        args: Optional[list[str]] = None,          # 추가 런치 플래그
        channel: Optional[str] = None,             # 예: "chrome" (실제 크롬 실행)
        proxy: Optional[dict] = None,              # {"server": "...", "username": "...", "password": "..."}
        locale: str = "ko-KR",                     # 기본 로케일
        timezone_id: str = "Asia/Seoul",           # 기본 타임존
        default_timeout_ms: int = 10000,           # 기본 타임아웃(ms)
    ):
        self.browser_type = browser_type
        self.headless = headless
        self.viewport = viewport
        self.args = args
        self.channel = channel
        self.proxy = proxy
        self.locale = locale
        self.timezone_id = timezone_id
        self.default_timeout_ms = default_timeout_ms

        self.pw: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    # with 구문 지원
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()

    def start(self) -> Page:
        """브라우저/컨텍스트/페이지를 초기화"""
        self.pw = sync_playwright().start()

        launcher = getattr(self.pw, self.browser_type, None)
        if launcher is None:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

        self.browser = launcher.launch(
            headless=self.headless,
            args=self.args,
            channel=self.channel,
            proxy=self.proxy,
        )

        w, h = self.viewport
        self.context = self.browser.new_context(
            viewport={"width": w, "height": h},
            locale=self.locale,
            timezone_id=self.timezone_id,
            accept_downloads=True,
        )
        self.context.set_default_timeout(self.default_timeout_ms)
        self.page = self.context.new_page()
        return self.page

    def stop(self):
        """리소스를 안전하게 정리"""
        for obj, closer in [
            (self.context, "close"),
            (self.browser, "close"),
            (self.pw, "stop"),
        ]:
            if obj:
                try:
                    getattr(obj, closer)()
                except Exception:
                    pass