# Playwright 기반 웹 UI 테스트 자동화 프로젝트

Python, Playwright, Pytest를 활용하여 **네이버 웹 서비스의 주요 UI와 사용자 흐름을 검증하는 개인 프로젝트**입니다.

로그인, 검색, 페이지 이동 기능을 테스트 대상으로 선정하고, **Page Object Model(POM)** 패턴으로 테스트 시나리오와 페이지 조작 로직을 분리했습니다. 테스트 코드를 읽기 쉽게 구성하고, UI 요소나 동작 방식이 변경될 때 수정할 위치를 명확히 하는 데 중점을 두었습니다.

> **프로젝트 범위:** 현재 공개된 코드는 **웹 브라우저 UI 테스트**를 대상으로 합니다. 모바일 앱 연동이나 실제 로그인 성공 검증은 포함하지 않습니다.

---

## 1. 프로젝트 개요

| 항목 | 내용 |
| --- | --- |
| 테스트 대상 | 네이버 웹 서비스 |
| 테스트 영역 | 로그인 UI·입력값, 검색, 메뉴 이동 |
| 테스트 방식 | Playwright 기반 브라우저 UI 자동화 |
| 테스트 실행 | Pytest |
| 설계 방식 | POM, Locator 분리, 공통 브라우저 관리 |
| 정의된 테스트 | 총 10개 (로그인 5개, 검색 2개, 네비게이션 3개) |

**구현한 내용**

- 테스트 시나리오와 페이지 조작 로직을 분리한 POM 구조
- UI 요소를 별도 모듈에서 관리하는 Locator 구성
- 공통 브라우저 실행·종료 및 환경 설정을 담당하는 `PlaywrightClient`
- 기능별 Pytest 테스트와 검증 결과를 확인하는 Assertion
- TestRail 테스트 케이스 ID를 표시하는 데코레이터 적용

---

## 2. 기술 스택

- **Python** — 테스트 및 공통 모듈 작성
- **Playwright (Sync API)** — 브라우저 조작 및 UI 상태 확인
- **Pytest** — 테스트 수집·실행, Fixture, Assertion
- **pytest-testrail** — 테스트 코드에 TestRail 케이스 ID 연결
- **Git / GitHub** — 버전 관리

> TestRail 케이스 ID는 코드에 연결되어 있으나, 이 저장소만으로 **TestRail 서버에 테스트 결과가 업로드되는 것까지 검증했다는 의미는 아닙니다.**

---

## 3. 프로젝트 구조 및 설계

```text
portfolio-test-automation/
├── common/
│   └── playwright.py          # 브라우저·컨텍스트·페이지 생성 및 종료
├── locator/
│   ├── login.py               # 로그인 UI 요소
│   ├── search.py              # 검색 UI 요소
│   └── navigation.py          # 주요 메뉴 및 예상 URL
├── pages/
│   ├── login_page.py          # 로그인 페이지 동작 및 상태 확인
│   ├── search_page.py         # 검색 동작 및 결과 페이지 확인
│   └── navigation_page.py     # 메뉴 클릭·새 탭 처리·URL 확인
├── tests/
│   ├── conftest.py            # 공통 Pytest Fixture
│   ├── test_login.py          # 로그인 관련 테스트
│   ├── test_search.py         # 검색 관련 테스트
│   └── test_navigation.py     # 메뉴 이동 관련 테스트
├── .gitignore                  # 로컬 환경 파일 등 Git 제외 규칙
└── README.md
```

### POM 적용

- **`tests/`**: 테스트 목적, 실행 순서, 기대 결과를 검증하는 코드
- **`pages/`**: 클릭·입력·페이지 이동·상태 확인 등 화면 조작 로직
- **`locator/`**: 페이지별 UI 요소와 예상 URL 정의
- **`common/`**: Playwright 브라우저 실행 및 리소스 관리

예를 들어 로그인 버튼의 위치가 변경되면 해당 Locator 또는 Page Object를 먼저 확인하도록 역할을 분리했습니다.

### 브라우저 실행 환경

`tests/conftest.py`에서 세션 범위 Fixture로 `PlaywrightClient`를 생성·종료합니다. 현재 설정은 다음과 같습니다.

- 브라우저: **Chromium** (클라이언트 기본값)
- 실행 모드: **headed (`headless=False`)** — 브라우저 창 표시
- 뷰포트: **1920 × 1080**
- 기본 로케일: `ko-KR`, 타임존: `Asia/Seoul`

현재는 하나의 세션에서 브라우저 컨텍스트와 페이지를 재사용합니다. 테스트 간 상태 격리는 향후 개선 과제로 두고 있습니다.

---

## 4. 테스트 시나리오

| 영역 | 테스트 목적 | 테스트 코드 |
| --- | --- | --- |
| 로그인 | 메인 페이지 로그인 버튼 노출 | `test_main_login_button_visible` |
| 로그인 | 로그인 화면 버튼 노출 | `test_form_login_button_visible` |
| 로그인 | 예시 ID·비밀번호 입력값 확인 | `test_naver_login_credentials_input` |
| 로그인 | 잘못된 계정의 인증 실패 흐름 | `test_naver_login_invalid_credentials` **(Skip)** |
| 로그인 | ID·비밀번호 미입력 시 입력 요청 메시지 노출 | `test_naver_login_empty_credentials` |
| 검색 | 검색 입력창과 버튼 노출 | `test_search_input_and_button_visible` |
| 검색 | 검색어 입력 후 결과 페이지로 이동 | `test_search_functionality_redirect` |
| 이동 | 카페 메뉴 클릭 후 새 탭 URL 확인 | `test_navigation_cafe` |
| 이동 | 블로그 메뉴 클릭 후 새 탭 URL 확인 | `test_navigation_blog` |
| 이동 | 증권 메뉴 클릭 후 새 탭 URL 확인 | `test_navigation_finance` |

**테스트 코드 바로가기:** [로그인](tests/test_login.py) · [검색](tests/test_search.py) · [네비게이션](tests/test_navigation.py)

### 검증 범위와 제한사항

- 로그인 테스트에는 **실제 계정 정보**를 사용하지 않습니다.
- 정상 로그인 성공 여부는 현재 테스트 범위에서 제외합니다.
- 잘못된 ID·비밀번호로 실제 인증을 요청하는 테스트는 CAPTCHA가 발생하여 `@pytest.mark.skip`으로 제외했습니다.
- 미입력 테스트는 버튼의 비활성화 여부가 아니라 **로그인 버튼 클릭 후 입력 요청 메시지가 나타나는지** 확인합니다.
- 외부 웹 서비스의 UI나 인증 정책이 변경되면 Locator 또는 기대 결과를 수정해야 할 수 있습니다.

---

## 5. 테스트 설계 및 구현 원칙

### ① 검증 목적과 기대 결과 명확화

테스트명과 Assertion으로 무엇을 확인하는지 드러내도록 작성했습니다. 예를 들어 검색 UI 테스트는 검색창과 검색 버튼이 화면에 존재하는지를 함께 확인합니다.

> 현재 프로젝트는 **'테스트마다 Assertion이 반드시 하나'라는 규칙을 적용하지 않습니다.** 하나의 검증 목적을 확인하는 데 필요한 경우 여러 Assertion을 사용할 수 있습니다.

### ② 테스트 로직과 화면 조작 분리

테스트 함수에서는 검증 흐름을 읽을 수 있도록 하고, 실제 클릭·입력·이동 동작은 Page Object가 담당하도록 했습니다.

```python
from pytest_testrail.plugin import pytestrail
from pages.login_page import NaverLogin


@pytestrail.case('C10001')
def test_main_login_button_visible(playwright_client):
    login_page = NaverLogin(playwright_client.page)
    login_page.go_to_naver_page()

    assert login_page.main_login_button_visible(), (
        "메인 페이지에 로그인 버튼이 노출되어야 함"
    )
```

### ③ 상황에 맞는 대기 및 새 탭 처리

- 로그인 화면에서는 Playwright의 `expect(...).to_be_visible()`로 요소 표시를 기다립니다.
- 검색 결과 이동에서는 로드 상태를 확인하는 대기를 사용합니다.
- 카페·블로그·증권 메뉴 이동에서는 `expect_page()`로 새 탭을 감지하고 URL을 검증합니다.

---

## 6. 설치 및 실행 방법

### 실행 전 준비

- Python **3.10 이상** 권장 (`pytest-testrail` 최신 버전의 요구사항 기준)
- Windows PowerShell 예시
- 테스트 대상 사이트에 접속할 수 있는 네트워크 환경

현재 공개 저장소에는 `requirements.txt`가 없으므로, 아래는 **코드에서 확인한 의존성을 직접 설치하는 방법**입니다.

```powershell
# 1. 저장소 복제
git clone https://github.com/HEECHANG96/portfolio-test-automation.git
cd portfolio-test-automation

# 2. 가상환경 생성 및 활성화
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. 필요한 패키지 설치
python -m pip install pytest playwright pytest-testrail

# 4. Chromium 브라우저 설치
python -m playwright install chromium

# 5. 전체 테스트 실행
python -m pytest tests/ -v
```

**일부 테스트만 실행**

```powershell
python -m pytest tests/test_login.py -v
python -m pytest tests/test_search.py -v
python -m pytest tests/test_navigation.py -v
```

**JUnit XML 결과 생성**

```powershell
New-Item -ItemType Directory -Force reports | Out-Null
python -m pytest tests/ -v --junitxml=reports/result.xml
```

위 명령어는 실행 방법의 예시입니다. **외부 사이트 상태와 로컬 환경에 따라 실제 PASS/FAIL 결과는 달라질 수 있으며, 이 README는 모든 테스트의 통과를 보장하지 않습니다.**

---

## 7. 실행 결과 확인 및 프로젝트 한계

현재 저장소에 **10개 테스트 함수가 정의**되어 있고, 그중 **1개는 CAPTCHA로 인한 Skip이 코드에 명시**되어 있습니다. 나머지 테스트의 PASS/FAIL은 실행 환경 및 네이버 웹 UI 상태에 따라 확인해야 합니다.

이번 README에는 별도로 검증되지 않은 성공률·실행시간 단축률을 기록하지 않았습니다. 실행 결과는 위 명령어의 Pytest 출력 또는 JUnit XML을 통해 확인할 수 있습니다.

**현재 한계**

- 특정 외부 웹 서비스의 UI 구조에 의존
- 일부 Locator가 XPath와 클래스명에 의존하여 UI 변경 시 실패 가능
- 세션 범위 Fixture로 브라우저 컨텍스트를 재사용
- 실제 로그인 및 CAPTCHA 우회 시나리오 미포함
- CI 환경에서의 자동 실행 및 TestRail 결과 업로드는 별도 검증 필요

---

## 8. 향후 개선 계획

1. `requirements.txt`를 추가하고 로컬 실행 절차 재검증
2. 테스트 간 브라우저 컨텍스트 격리 및 Fixture 구조 개선
3. UI 변경에 대응하기 쉬운 Locator와 대기 전략 보완
4. GitHub Actions로 자동 실행 및 결과 수집 환경 구성
5. JUnit XML 결과를 별도 프로젝트인 **[qa-result-analyzer](https://github.com/HEECHANG96/qa-result-analyzer)**와 연결해 실패 유형을 분석하는 흐름 검증

> 위 항목은 **향후 계획**이며, 현재 구현이 완료되었다는 의미가 아닙니다.

---

## 9. 프로젝트를 통해 확인한 점

- 테스트 코드와 화면 조작 로직을 분리하면 기능별 역할과 수정 위치가 분명해집니다.
- 테스트의 개수보다 **검증 목적과 실제 Assertion의 일치**가 중요합니다.
- 외부 서비스를 대상으로 한 UI 자동화에서는 사이트 변경, 인증 정책, 실행 환경에 따른 실패를 구분해 다뤄야 합니다.
- 자동화 테스트를 작성하는 것뿐 아니라 **실패 원인을 이해하고 실행 결과를 재현 가능하게 남기는 과정**도 중요하다고 생각합니다.

---

**관련 프로젝트:** [qa-result-analyzer — JUnit XML 테스트 결과 분석](https://github.com/HEECHANG96/qa-result-analyzer)