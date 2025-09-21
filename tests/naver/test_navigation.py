from pytest_testrail.plugin import pytestrail
from locator.naver.navigation import Navigation
from tests.naver.utils.navigation import NaverNavigation


@pytestrail.case('C30001')
def test_navigation_cafe(playwright_client):
    client = playwright_client
    nav_util = NaverNavigation(client.page)

    # 1. 메인 페이지 이동
    nav_util.go_to_naver_page()

    # 2. 카페 메뉴 클릭 후 새 탭에서 로드 완료 대기
    new_tab = nav_util.click_and_wait(Navigation.CAFE_BTN)

    # 3. 새 탭에서 URL이 기대한 카페 URL인지 검증
    assert nav_util.is_correct_page(new_tab, Navigation.CAFE_URL)


@pytestrail.case('C30002')
def test_navigation_blog(playwright_client):
    client = playwright_client
    nav_util = NaverNavigation(client.page)

    # 1. 메인 페이지 이동
    nav_util.go_to_naver_page()

    # 2. 블로그 메뉴 클릭 후 새 탭에서 로드 완료 대기
    new_tab = nav_util.click_and_wait(Navigation.BLOG_BTN)

    # 3. 새 탭에서 URL이 기대한 블로그 URL인지 검증
    assert nav_util.is_correct_page(new_tab, Navigation.BLOG_URL)


@pytestrail.case('C30003')
def test_navigation_finance(playwright_client):
    client = playwright_client
    nav_util = NaverNavigation(client.page)

    # 1. 메인 페이지 이동
    nav_util.go_to_naver_page()

    # 2. 증권 메뉴 클릭 후 새 탭에서 로드 완료 대기
    new_tab = nav_util.click_and_wait(Navigation.FINANCE_BTN)

    # 3. 새 탭에서 URL이 기대한 증권 URL인지 검증
    assert nav_util.is_correct_page(new_tab, Navigation.FINANCE_URL)
