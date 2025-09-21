class Navigation:
    # 네이버 메인 메뉴 네비게이션 버튼
    CAFE_BTN = {"type": "XPATH", "value": '//a[span[@class="service_name" and text()="카페"]]'}
    BLOG_BTN = {"type": "XPATH", "value": '//a[span[@class="service_name" and text()="블로그"]]'}
    FINANCE_BTN = {"type": "XPATH", "value": '//a[span[@class="service_name" and text()="증권"]]'}

    CAFE_URL = 'https://section.cafe.naver.com/'
    BLOG_URL = 'https://section.blog.naver.com/'
    FINANCE_URL = 'https://finance.naver.com/'

    CAFE_TITLE = {"type": "XPATH", "value": '//a[span[@class="service_name" and text()="카페"]]'}
    BLOG_TITLE = {"type": "XPATH", "value": '//a[span[@class="service_name" and text()="블로그"]]'}
    FINANCE_TITLE = {"type": "XPATH", "value": '//span[@class="tx" and text()="증권 홈"]'}