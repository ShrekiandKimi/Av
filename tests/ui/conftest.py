import pytest
from playwright.sync_api import Page, BrowserContext, expect
import time
import random

BASE_URL = "https://cerulean-praline-8e5aa6.netlify.app"


@pytest.fixture(scope="session")
def base_url(request):
    """Получение базового URL из командной строки или использование значения по умолчанию"""
    return request.config.getoption("--base-url") or BASE_URL


@pytest.fixture(scope="function")
def desktop_viewport(context: BrowserContext):
    """Настройка viewport для десктопных тестов (1920x1080)"""
    context.set_viewport_size({"width": 1920, "height": 1080})
    yield context


@pytest.fixture(scope="function")
def mobile_viewport(context: BrowserContext):
    """Настройка viewport для мобильных тестов (375x812 - iPhone SE)"""
    context.set_viewport_size({"width": 375, "height": 812})
    context.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    })
    yield context


@pytest.fixture
def wait_for_page_load(page: Page):
    """Хелпер для ожидания загрузки страницы"""
    def _wait(timeout=30000):
        page.wait_for_load_state("networkidle", timeout=timeout)
    return _wait


@pytest.fixture
def wait_for_element(page: Page):
    """Хелпер для ожидания появления элемента"""
    def _wait(selector, timeout=10000, state="visible"):
        page.wait_for_selector(selector, state=state, timeout=timeout)
    return _wait


@pytest.fixture
def clear_local_storage(page: Page):
    """Очистка localStorage перед тестом"""
    page.evaluate("() => localStorage.clear()")
    yield
    page.evaluate("() => localStorage.clear()")


@pytest.fixture
def random_delay():
    """Случайная задержка для избежания rate limiting"""
    def _delay(min_ms=500, max_ms=1500):
        time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))
    return _delay


@pytest.fixture(scope="function")
def desktop_page(page: Page, desktop_viewport, wait_for_page_load):
    """Фикстура для десктопных тестов"""
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)
    yield page


@pytest.fixture(scope="function")
def mobile_page(page: Page, mobile_viewport, wait_for_page_load):
    """Фикстура для мобильных тестов"""
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)
    yield page


@pytest.fixture
def capture_screenshot(page: Page, request):
    """Фикстура для создания скриншотов при падении теста"""
    yield
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        screenshot_path = f"test-results/{request.node.name}-failure.png"
        page.screenshot(path=screenshot_path, full_page=True)


def pytest_runtest_makereport(item, call):
    """Хук для отслеживания статуса тестов"""
    if call.when == "call":
        item.rep_call = call
    elif call.when == "setup":
        item.rep_setup = call
    elif call.when == "teardown":
        item.rep_teardown = call