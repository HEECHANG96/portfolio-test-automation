
import pytest

from common.playwright import PlaywrightClient


@pytest.fixture(scope="function")
def playwright_client():
    client = PlaywrightClient(
        headless=False,
        viewport=(1920, 1080)
    )

    # 테스트 시작 전 브라우저 생성
    client.start()

    try:
        yield client
    finally:
        # 테스트 종료 후 브라우저 및 리소스 정리
        client.stop()
