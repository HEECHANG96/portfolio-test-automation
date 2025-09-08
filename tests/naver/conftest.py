import pytest
from common.playwright import PlaywrightClient


@pytest.fixture(scope="session")
def playwright_client():
    # 여기서 실행 환경에 맞춰 인자 조정
    client = PlaywrightClient(headless=False, width=1920, height=1080)

    # 실제로 Playwright를 시작하고 브라우저/컨텍스트/페이지를 연다.
    client.start_browser()
    yield client
    # yield 이후의 코드는 테스트가 모두 끝난 뒤(세션 종료 시) 실행된다.
    client.stop()
