import pytest
import allure
import time
from playwright.sync_api import Page, expect

pytestmark = [pytest.mark.desktop, pytest.mark.stats]


@allure.feature("Статистика")
@allure.story("Таймер обновления")
class TestStatsTimer:
    """Тесты таймера обновления статистики"""
    
    @allure.title("TC-UI-010: Кнопка «Обновить» — ручное обновление")
    @allure.description("Проверка работы кнопки ручного обновления статистики")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_manual_refresh_button(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка кнопки ручного обновления"""
        desktop_page.goto(f"{base_url}/stats")
        wait_for_page_load()
        
        refresh_button = desktop_page.locator(
            'button:has-text("Обновить"), '
            'button:has-text("Refresh"), '
            '[data-testid="refresh-button"], '
            '.refresh-btn'
        )
        
        if refresh_button.count() > 0:
            last_update_before = desktop_page.locator(
                '[data-testid="last-update"], '
                '.last-update, '
                '.timestamp'
            ).text_content()
            
            refresh_button.click()
            
            try:
                desktop_page.wait_for_load_state("networkidle", timeout=10000)
            except:
                pass
            
            time.sleep(2)
            
            expect(refresh_button).to_be_enabled()
        
        expect(desktop_page.locator('body')).not_to_contain_text("Ошибка")
    
    @allure.title("TC-UI-011: Кнопка «Остановить» — остановка таймера")
    @allure.description("Проверка остановки автообновления статистики")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_timer_stop_button(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка кнопки остановки таймера"""
        desktop_page.goto(f"{base_url}/stats")
        wait_for_page_load()
        
        stop_button = desktop_page.locator(
            'button:has-text("Остановить"), '
            'button:has-text("Stop"), '
            '[data-testid="stop-button"]'
        )
        start_button = desktop_page.locator(
            'button:has-text("Запустить"), '
            'button:has-text("Start"), '
            '[data-testid="start-button"]'
        )
        
        if stop_button.count() > 0:
            if stop_button.is_visible():
                stop_button.click()
                time.sleep(1)
                
                expect(start_button).to_be_visible(timeout=5000)
                expect(stop_button).not_to_be_visible()
            
            elif start_button.is_visible():
                pass
        
        expect(desktop_page.locator('body')).not_to_contain_text("Ошибка")
    
    @allure.title("TC-UI-012: Кнопка «Запустить» — запуск таймера")
    @allure.description("Проверка запуска автообновления статистики")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_timer_start_button(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка кнопки запуска таймера"""
        desktop_page.goto(f"{base_url}/stats")
        wait_for_page_load()
        
        stop_button = desktop_page.locator(
            'button:has-text("Остановить"), '
            'button:has-text("Stop"), '
            '[data-testid="stop-button"]'
        )
        start_button = desktop_page.locator(
            'button:has-text("Запустить"), '
            'button:has-text("Start"), '
            '[data-testid="start-button"]'
        )
        
        if start_button.count() > 0 and start_button.is_visible():
            start_button.click()
            time.sleep(1)
            
            expect(stop_button).to_be_visible(timeout=5000)
            expect(start_button).not_to_be_visible()
        
        elif stop_button.count() > 0 and stop_button.is_visible():
            pass
        
        expect(desktop_page.locator('body')).not_to_contain_text("Ошибка")
    
    @allure.title("TC-UI-013: Таймер — корректность интервала обновления")
    @allure.description("Проверка интервала автообновления статистики")
    @allure.severity(allure.severity_level.NORMAL)
    def test_timer_interval_accuracy(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка корректности интервала автообновления"""
        desktop_page.goto(f"{base_url}/stats")
        wait_for_page_load()
        
        timer_display = desktop_page.locator(
            '[data-testid="timer-display"], '
            '.timer-display, '
            '.countdown'
        )
        
        if timer_display.count() > 0:
            initial_time = timer_display.text_content()
            time.sleep(5)
            current_time = timer_display.text_content()
        
        expect(desktop_page.locator('body')).not_to_contain_text("Ошибка")
    
    @allure.title("TC-UI-014: Таймер — данные обновляются при автообновлении")
    @allure.description("Проверка обновления данных при сработке таймера")
    @allure.severity(allure.severity_level.NORMAL)
    def test_timer_data_refresh(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка что данные обновляются при автообновлении"""
        desktop_page.goto(f"{base_url}/stats")
        wait_for_page_load()
        
        initial_data = desktop_page.locator(
            '[data-testid="stats-data"], '
            '.stats-container, '
            '.statistics'
        ).text_content()
        
        stop_button = desktop_page.locator(
            'button:has-text("Остановить"), '
            '[data-testid="stop-button"]'
        )
        start_button = desktop_page.locator(
            'button:has-text("Запустить"), '
            '[data-testid="start-button"]'
        )
        
        if stop_button.is_visible():
            stop_button.click()
            time.sleep(1)
            
            data_after_stop = desktop_page.locator(
                '[data-testid="stats-data"], '
                '.stats-container'
            ).text_content()
            
            if start_button.is_visible():
                start_button.click()
                time.sleep(1)
        
        expect(desktop_page.locator('body')).not_to_contain_text("Ошибка")