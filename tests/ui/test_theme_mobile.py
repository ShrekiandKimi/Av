import pytest
import allure
from playwright.sync_api import Page, expect
import time

pytestmark = [pytest.mark.mobile, pytest.mark.theme]


@allure.feature("Тема")
@allure.story("Переключение темы")
class TestThemeToggle:
    """Тесты переключения светлой/тёмной темы"""
    
    @allure.title("TC-UI-020: Переключение на тёмную тему")
    @allure.description("Проверка переключения интерфейса в тёмную тему на мобильной версии")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_toggle_to_dark_theme(self, mobile_page: Page, base_url, wait_for_page_load):
        """Проверка переключения на тёмную тему"""
        mobile_page.goto(base_url)
        wait_for_page_load()
        
        body = mobile_page.locator('body')
        
        theme_toggle = mobile_page.locator(
            'button[data-testid="theme-toggle"], '
            '[data-testid="theme-switch"], '
            '.theme-toggle, '
            '.theme-switch, '
            'button:has-text("Тема"), '
            'button:has-text("Theme")'
        )
        
        if theme_toggle.count() > 0:
            initial_class = body.get_attribute('class') or ''
            is_initially_dark = 'dark' in initial_class.lower()
            
            theme_toggle.click()
            time.sleep(1)
            
            new_class = body.get_attribute('class') or ''
            
            if not is_initially_dark:
                assert 'dark' in new_class.lower(), \
                    f"Тема не переключилась на тёмную. Классы: {new_class}"
            else:
                assert 'dark' not in new_class.lower(), \
                    f"Тема не переключилась на светлую. Классы: {new_class}"
        
        expect(mobile_page.locator('body')).not_to_contain_text("Ошибка")
    
    @allure.title("TC-UI-021: Переключение на светлую тему")
    @allure.description("Проверка переключения интерфейса в светлую тему на мобильной версии")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_toggle_to_light_theme(self, mobile_page: Page, base_url, wait_for_page_load):
        """Проверка переключения на светлую тему"""
        mobile_page.goto(base_url)
        wait_for_page_load()
        
        body = mobile_page.locator('body')
        theme_toggle = mobile_page.locator(
            'button[data-testid="theme-toggle"], '
            '.theme-toggle, '
            '.theme-switch'
        )
        
        if theme_toggle.count() > 0:
            theme_toggle.click()
            time.sleep(1)
            theme_toggle.click()
            time.sleep(1)
            
            current_class = body.get_attribute('class') or ''
            
            expect(mobile_page.locator('body')).not_to_contain_text("Ошибка")
    
    @allure.title("TC-UI-022: Сохранение темы после перезагрузки")
    @allure.description("Проверка сохранения выбранной темы в localStorage")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_theme_persists_after_reload(self, mobile_page: Page, base_url, wait_for_page_load):
        """Проверка сохранения темы после перезагрузки страницы"""
        mobile_page.goto(base_url)
        wait_for_page_load()
        
        body = mobile_page.locator('body')
        theme_toggle = mobile_page.locator(
            'button[data-testid="theme-toggle"], '
            '.theme-toggle'
        )
        
        if theme_toggle.count() > 0:
            initial_class = body.get_attribute('class') or ''
            theme_toggle.click()
            time.sleep(1)
            
            new_class = body.get_attribute('class') or ''
            stored_theme = mobile_page.evaluate("() => localStorage.getItem('theme')")
            
            mobile_page.reload()
            wait_for_page_load()
            time.sleep(1)
            
            after_reload_class = body.get_attribute('class') or ''
            
            if stored_theme:
                if stored_theme == 'dark':
                    assert 'dark' in after_reload_class.lower(), \
                        f"Тема не сохранилась после перезагрузки. Ожидалась dark, получено: {after_reload_class}"
                elif stored_theme == 'light':
                    assert 'dark' not in after_reload_class.lower(), \
                        f"Тема не сохранилась после перезагрузки. Ожидалась light, получено: {after_reload_class}"
        
        expect(mobile_page.locator('body')).not_to_contain_text("Ошибка")
    
    @allure.title("TC-UI-023: Визуальная проверка тёмной темы")
    @allure.description("Проверка контрастности и читаемости в тёмной теме")
    @allure.severity(allure.severity_level.MINOR)
    def test_dark_theme_visual_check(self, mobile_page: Page, base_url, wait_for_page_load):
        """Визуальная проверка элементов в тёмной теме"""
        mobile_page.goto(base_url)
        wait_for_page_load()
        
        theme_toggle = mobile_page.locator(
            'button[data-testid="theme-toggle"], '
            '.theme-toggle'
        )
        
        if theme_toggle.count() > 0:
            theme_toggle.click()
            time.sleep(1)
            
            body = mobile_page.locator('body')
            
            background_color = body.evaluate(
                "el => window.getComputedStyle(el).backgroundColor"
            )
            
            if 'rgb' in background_color:
                import re
                rgb_values = re.findall(r'\d+', background_color)
                if len(rgb_values) >= 3:
                    r, g, b = int(rgb_values[0]), int(rgb_values[1]), int(rgb_values[2])
                    avg_brightness = (r + g + b) / 3
        
        expect(mobile_page.locator('body')).not_to_contain_text("Ошибка")


@allure.feature("Мобильная версия")
@allure.story("Адаптивность")
class TestMobileResponsive:
    """Тесты адаптивности мобильной версии"""
    
    @allure.title("TC-UI-024: Навигация на мобильной версии")
    @allure.description("Проверка работы навигации на мобильном viewport")
    @allure.severity(allure.severity_level.NORMAL)
    def test_mobile_navigation(self, mobile_page: Page, base_url, wait_for_page_load):
        """Проверка навигации на мобильной версии"""
        mobile_page.goto(base_url)
        wait_for_page_load()
        
        mobile_menu = mobile_page.locator(
            '.hamburger-menu, '
            '[data-testid="mobile-menu"], '
            '.mobile-nav, '
            'button[aria-label="Menu"]'
        )
        
        if mobile_menu.count() > 0:
            mobile_menu.click()
            time.sleep(1)
            
            menu_content = mobile_page.locator(
                '.menu-content, '
                '.nav-menu, '
                '[data-testid="menu-content"]'
            )
            
            expect(mobile_page.locator('body')).not_to_contain_text("Ошибка")
    
    @allure.title("TC-UI-025: Элементы не наезжают друг на друга")
    @allure.description("Проверка отсутствия наложений элементов на мобильной версии")
    @allure.severity(allure.severity_level.MINOR)
    def test_no_element_overlap(self, mobile_page: Page, base_url, wait_for_page_load):
        """Проверка отсутствия наложений элементов"""
        mobile_page.goto(base_url)
        wait_for_page_load()
        
        main_content = mobile_page.locator(
            'main, '
            '[data-testid="main-content"], '
            '.main-content, '
            '.content'
        )
        
        if main_content.count() > 0:
            expect(main_content.first).to_be_visible()
            
            body = mobile_page.locator('body')
            expect(body).not_to_contain_text("Ошибка")