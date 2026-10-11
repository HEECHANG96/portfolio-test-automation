# Playwright 기반 웹 UI 테스트 자동화 프로젝트

Python, Playwright, Pytest를 활용하여 **네이버 웹 서비스의 로그인·검색·페이지 이동 기능을 검증하는 개인 테스트 자동화 프로젝트**입니다.

테스트 시나리오와 페이지 조작 로직을 **Page Object Model(POM)** 패턴으로 분리하고, Locator와 브라우저 실행 환경을 별도로 관리하도록 구성했습니다. 외부 서비스의 UI 변경으로 테스트가 실패했을 때 로그를 분석하고, 변경된 사용자 동작에 맞춰 테스트를 개선하는 과정도 포함합니다.

> **프로젝트 범위:** 현재 구현 범위는 **PC 웹 브라우저 UI 테스트**입니다. 모바일 앱 연동, 실제 계정의 로그인 성공 검증, TestRail 서버로의 결과 업로드는 포함하지 않습니다.

---

## 1. 프로젝트 개요

| 항목 | 내용 |
| --- | --- |
| 테스트 대상 | 네이버 웹 서비스 |
| 테스트 영역 | 로그인 UI·입력값, 검색, 주요 메뉴 이동 |
| 자동화 도구 | Playwright (Python Sync API), Pytest |
| 설계 방식 | POM, 페이지별 Locator 분리, Pytest Fixture |
| 테스트 규모 | 총 10개: 로그인 5개, 검색 2개, 네비게이션 3개 |
| 검증 환경 | Windows, Python 3.12.3, Chromium |
| 최근 로컬 실행 결과 | **9 PASS · 0 FAIL · 1 SKIP** (40.08초) |

**주요 구현 내용**

- 기능별 테스트(`tests/`)와 페이지 조작(`pages/`) 및 UI 요소(`locator/`) 분리
- `PlaywrightClient`를 통한 브라우저·컨텍스트·페이지 초기화 및 정리
- `scope="function"` Fixture를 활용한 테스트별 독립 실행 환경 구성
- 테스트 목적에 맞춘 Assertion, URL 검증 및 새 탭 처리
- `pytest-testrail` 데코레이터를 이용한 테스트 케이스 ID 매핑
- Pytest의 JUnit XML 출력 지원

---

## 2. 기술 스택

| 기술 | 프로젝트 내 역할 |
| --- | --- |
| Python | 테스트 코드 및 공통 모듈 작성 |
| Playwright | Chromium 브라우저 조작, 요소 확인, 입력, 페이지 이동 |
| Pytest | 테스트 수집·실행, Fixture, Assertion, Skip 관리 |
| pytest-testrail | 코드에 TestRail 케이스 ID 연결 |
| Git / GitHub | 변경 이력 및 브랜치 관리 |

로컬에서 확인한 직접 의존성 버전은 `requirements.txt`로 관리합니다.

```text
pytest==8.4.1
playwright==1.54.0
pytest-testrail==2.9.0
```

> **TestRail 연동 범위:** 테스트 코드에 케이스 ID를 표시하는 데코레이터를 사용합니다. 실제 TestRail 서버로 실행 결과를 전송하는 기능은 이 프로젝트의 검증 범위에 포함하지 않습니다.

---

## 3. 프로젝트 구조 및 설계

```text
portfolio-test-automation/
├── common/
│   └── playwright.py          # 브라우저·컨텍스트·페이지 생성 및 종료
├── locator/
│   ├── login.py               # 로그인 UI 요소
│   ├── search.py              # 검색 입력창 Locator
│   └── navigation.py          # 메뉴 Locator 및 예상 URL
├── pages/
│   ├── login_page.py          # 로그인 관련 동작 및 상태 확인
│   ├── search_page.py         # 검색어 입력·Enter·결과 페이지 확인
│   └── navigation_page.py     # 메뉴 클릭·새 탭·URL 확인
├── tests/
│   ├── conftest.py            # 공통 Pytest Fixture
│   ├── test_login.py          # 로그인 테스트 5개
│   ├── test_search.py         # 검색 테스트 2개
│   └── test_navigation.py     # 네비게이션 테스트 3개
├── .gitignore                 # 로컬 환경·실행 결과 제외
├── pytest.ini                 # Pytest 마커 설정
├── requirements.txt           # Python 패키지 의존성
└── README.md
```

### 3.1 POM 기반 역할 분리

- **`tests/`**: 사용자 시나리오, 검증 목적, 기대 결과와 Assertion 정의
- **`pages/`**: 페이지 이동, 입력, 클릭, UI 상태 확인 등의 동작 처리
- **`locator/`**: 페이지별 UI 요소와 예상 URL 관리
- **`common/`**: Playwright 실행 환경과 브라우저 리소스 관리

UI 구조가 변경되면 Locator와 Page Object를 중심으로 영향을 확인할 수 있도록 분리했습니다.

### 3.2 테스트별 브라우저 격리

`tests/conftest.py`에서 **`scope="function"` Fixture**를 사용하여 각 테스트가 시작될 때 `PlaywrightClient`를 생성하고, 종료 시 브라우저 관련 리소스를 정리합니다.

- 브라우저: Chromium
- 실행 모드: headed (`headless=False`)
- 뷰포트: 1920 × 1080
- 로케일: `ko-KR`
- 타임존: `Asia/Seoul`
- 테스트별 브라우저·컨텍스트·페이지 새로 생성 및 정리

이를 통해 이전 테스트의 페이지 이동이나 브라우저 상태가 다음 테스트에 영향을 줄 위험을 줄였습니다. 다만 **각 테스트마다 브라우저 전체를 실행**하므로 실행시간 측면에서는 추가 최적화 여지가 있습니다.

---

## 4. 테스트 시나리오

| 영역 | 검증 목적 | 테스트 함수 | 상태 |
| --- | --- | --- | --- |
| 로그인 | 메인 화면 로그인 버튼 노출 | `test_main_login_button_visible` | PASS |
| 로그인 | 로그인 화면의 버튼 노출 | `test_form_login_button_visible` | PASS |
| 로그인 | 예시 ID·비밀번호 입력값 반영 | `test_naver_login_credentials_input` | PASS |
| 로그인 | 잘못된 계정의 인증 실패 흐름 | `test_naver_login_invalid_credentials` | SKIP |
| 로그인 | ID·비밀번호 미입력 시 안내 메시지 노출 | `test_naver_login_empty_credentials` | PASS |
| 검색 | 메인 화면 검색 입력창 노출 | `test_search_input_visible` | PASS |
| 검색 | 검색어 입력 → Enter → 결과 페이지 이동 | `test_search_functionality_redirect` | PASS |
| 메뉴 이동 | 카페 메뉴 새 탭 이동 및 URL 확인 | `test_navigation_cafe` | PASS |
| 메뉴 이동 | 블로그 메뉴 새 탭 이동 및 URL 확인 | `test_navigation_blog` | PASS |
| 메뉴 이동 | 증권 메뉴 새 탭 이동 및 URL 확인 | `test_navigation_finance` | PASS |

**실제 코드:** [로그인](tests/test_login.py) · [검색](tests/test_search.py) · [네비게이션](tests/test_navigation.py)

### 검증 범위 및 예외 처리

- 로그인 테스트에는 실제 사용자 계정 정보를 사용하지 않습니다.
- 정상 로그인 성공 여부는 현재 검증 범위에 포함하지 않습니다.
- 잘못된 로그인 정보를 실제 제출하는 테스트는 CAPTCHA가 발생하므로 `@pytest.mark.skip`으로 제외합니다.
- 미입력 조건에서는 버튼 비활성화가 아니라 **버튼 클릭 후 입력 요청 메시지 노출**을 검증합니다.
- 검색 기능은 별도 버튼 클릭 대신 **검색 입력창에서 Enter 키를 누르는 사용자 동작**을 검증합니다.
- 외부 서비스의 UI나 URL 정책이 변경되면 Locator 및 기대 결과를 재검토해야 합니다.

---

## 5. 테스트 설계 및 구현 원칙

### 5.1 검증 목적이 드러나는 테스트 작성

테스트 함수명과 Assertion을 통해 무엇을 검증하는지 명확하게 표현했습니다. `1 TC = 1 Assertion`을 강제하지 않으며, **하나의 테스트 목적을 확인하는 데 필요한 경우 여러 Assertion을 사용할 수 있습니다.**

### 5.2 테스트 코드와 조작 로직 분리

테스트 코드에서는 사용자 흐름과 기대 결과를 확인하고, 클릭·입력·이동 등의 동작은 Page Object를 통해 수행합니다.

```python
from pytest_testrail.plugin import pytestrail
from pages.login_page import NaverLogin


@pytestrail.case("C10001")
def test_main_login_button_visible(playwright_client):
    login_page = NaverLogin(playwright_client.page)
    login_page.go_to_naver_page()

    assert login_page.main_login_button_visible(), (
        "메인 페이지에 로그인 버튼이 노출되어야 함"
    )
```

### 5.3 동작에 맞는 대기 조건 활용

- 로그인 요소 표시: Playwright의 가시성 검증(`expect(...).to_be_visible()`)
- 검색: Enter 입력 후 `wait_for_url()`로 결과 페이지 이동 확인
- 메뉴 이동: `expect_page()`로 새 탭 생성 감지 후 URL 확인

검색 흐름에서는 기존 `networkidle` 대기 대신 **검증 목적에 직접 대응하는 URL 이동 대기**를 사용합니다.

---

## 6. 설치 및 실행 방법

아래 명령어는 **Windows Git Bash** 기준입니다. Python 3.12.3 및 `requirements.txt`에 명시된 버전 조합으로 로컬 실행을 확인했습니다.

### 6.1 저장소 복제 및 가상환경 구성

```bash
git clone https://github.com/HEECHANG96/portfolio-test-automation.git
cd portfolio-test-automation

python -m venv .venv
source .venv/Scripts/activate
```

### 6.2 패키지 및 브라우저 설치

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

### 6.3 테스트 실행

```bash
# 전체 테스트
python -m pytest tests/ -v

# 검색 기능만 실행
python -m pytest tests/test_search.py -v

# 테스트 수집만 확인
python -m pytest tests/ --collect-only -q
```

### 6.4 JUnit XML 결과 생성

```bash
mkdir -p reports
python -m pytest tests/ -v --junitxml=reports/result.xml
```

생성되는 `reports/result.xml`에는 테스트 실행 결과가 저장됩니다. `reports/`는 `.gitignore`에 등록되어 있어 기본적으로 Git 관리 대상에서 제외합니다.

---

## 7. 로컬 테스트 실행 결과

**실행 환경:** Windows / Python 3.12.3 / Pytest 8.4.1 / Playwright 1.54.0 / Chromium

| 항목 | 결과 |
| --- | ---: |
| 전체 테스트 | 10개 |
| PASS | **9개** |
| FAIL | **0개** |
| SKIP | **1개** |
| 실행시간 | **40.08초** |

```text
9 passed, 1 skipped in 40.08s
```

- **SKIP 사유:** 잘못된 계정의 실제 인증 요청 시 CAPTCHA가 나타나 자동 검증 대상에서 제외했습니다.
- **결과 파일:** `reports/result.xml` (JUnit XML)
- **해석:** 실행된 9개 테스트가 통과했으며, SKIP된 인증 테스트가 성공했다는 의미는 아닙니다.

> 이 결과는 한 차례의 실제 로컬 실행 기록입니다. 네이버의 UI 변경, 네트워크 상태 및 실행 환경에 따라 이후 결과는 달라질 수 있습니다. 이 실행시간은 Selenium 대비 성능 향상 수치가 아닙니다.

---

## 8. 문제 해결 및 개선 경험

### 8.1 검색 UI 변경에 따른 테스트 복구

**문제**

기존 검색 자동화는 검색 버튼 내부의 `span` 요소를 Locator로 사용했습니다. 테스트 실행 중 요소가 DOM에서 찾아지더라도 화면에 표시되지 않아, 검색 버튼 노출 테스트는 실패하고 클릭 과정에서는 `TimeoutError`가 발생했습니다.

**원인 확인**

- Playwright 로그: Locator가 요소를 찾았으나 `element is not visible` 상태
- 현재 네이버 메인 화면의 검색 사용자 흐름과 기존 버튼 클릭 시나리오 불일치

**수정 내용**

1. 검색 버튼 Locator와 관련 Page Object 메서드 제거
2. 검색 입력창의 `id="query"`를 이용해 `#query` Locator 적용
3. 검색어 입력 후 `press("Enter")`로 검색 수행
4. `networkidle` 대신 `wait_for_url()`로 검색 결과 페이지 이동 확인
5. 변경된 검증 목적에 맞춰 테스트 함수명과 기대 결과 수정

**검증 결과**

- 수정한 검색 테스트 **2개 모두 PASS**
- 전체 회귀 테스트 **9 PASS · 0 FAIL · 1 SKIP** 확인

### 8.2 테스트 실행 환경 분리

기존에는 세션 범위 Fixture에서 브라우저를 공유했습니다. 테스트 간 페이지·세션 상태가 영향을 줄 위험을 줄이기 위해 `scope="function"`으로 변경하고, 각 테스트의 시작·종료 시 브라우저 리소스를 생성·정리하도록 개선했습니다.

이 변경만으로 검색 오류가 해결된 것은 아니며, **검색 테스트의 직접적인 복구는 위 Locator·시나리오 수정으로 확인**했습니다.

### 8.3 증권 메뉴 URL 변경 대응

증권 메뉴 이동 테스트에서 기대 URL(`https://finance.naver.com/`)과 실제 이동 URL(`https://stock.naver.com/`)이 달라 Assertion이 실패했습니다. 실제 이동 경로를 확인한 뒤 기대 URL을 수정하고 해당 테스트의 PASS를 확인했습니다.

---

## 9. 한계 및 향후 개선 계획

**현재 한계**

- 외부 웹 서비스의 UI 및 URL 구조에 의존
- 일부 Locator가 XPath·클래스명에 의존하여 구조 변경에 취약할 수 있음
- 테스트별 브라우저 전체 실행으로 인한 초기화 시간 발생
- 실제 로그인 성공 및 CAPTCHA가 발생하는 인증 흐름은 검증 대상에서 제외
- GitHub Actions 기반 자동 실행과 TestRail 결과 업로드는 미구현·미검증

**향후 계획**

1. 브라우저는 재사용하고 테스트별 `BrowserContext`를 분리하여 실행 효율 개선
2. Locator 선택 기준과 실패 시 진단 정보 보완
3. GitHub Actions를 이용한 자동 테스트 실행 및 결과 수집
4. 별도 프로젝트인 [qa-result-analyzer](https://github.com/HEECHANG96/qa-result-analyzer)로 JUnit XML을 분석하는 흐름 검증

> 향후 계획은 현재 구현 완료 기능과 구분하여 기재했습니다.

---

## 10. 프로젝트를 통해 배운 점

- 테스트 코드를 기능별로 분리하는 것뿐 아니라 **검증 목적과 기대 결과를 명확하게 유지하는 것**이 중요합니다.
- 외부 서비스 UI가 변경되면 단순히 타임아웃을 늘리기보다 **실제 사용자 동작과 Locator의 유효성**을 먼저 확인해야 합니다.
- 테스트 간 상태 공유를 줄이는 설계는 신뢰성에 중요하지만, 실행시간과의 균형도 고려해야 합니다.
- 단일 테스트의 복구로 끝내지 않고 **전체 회귀 테스트로 변경 영향을 확인**하는 과정이 필요합니다.

**관련 프로젝트:** [qa-result-analyzer — JUnit XML 테스트 결과 분석](https://github.com/HEECHANG96/qa-result-analyzer)
