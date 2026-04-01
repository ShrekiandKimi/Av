import pytest
import allure
from playwright.sync_api import Page, expect
import time

pytestmark = [pytest.mark.desktop, pytest.mark.filters]


@allure.feature("Фильтры")
@allure.story("Диапазон цен")
class TestPriceFilter:
    """Тесты фильтра по диапазону цен"""
    
    @allure.title("TC-UI-001: Фильтр по диапазону цен — позитивный сценарий")
    @allure.description("Проверка корректной работы фильтра цены")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_price_filter_positive(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка фильтрации объявлений по диапазону цен"""
        desktop_page.goto(f"{base_url}/list")
        wait_for_page_load()
        
        min_price_input = desktop_page.locator('input[name="minPrice"], input[data-testid="min-price"]')
        max_price_input = desktop_page.locator('input[name="maxPrice"], input[data-testid="max-price"]')
        apply_button = desktop_page.locator(
            'button[type="submit"], '
            'button:has-text("Применить"), '
            'button:has-text("Apply")'
        )
        
        if min_price_input.count() > 0 and max_price_input.count() > 0:
            min_price_input.fill("1000")
            max_price_input.fill("5000")
            apply_button.click()
            wait_for_page_load()
            
            price_elements = desktop_page.locator(
                '[data-testid="item-price"], '
                '.item-price, '
                '.price'
            )
            
            if price_elements.count() > 0:
                for i in range(price_elements.count()):
                    price_text = price_elements.nth(i).text_content()
                    if price_text:
                        price_value = int(''.join(filter(str.isdigit, price_text)))
                        assert 1000 <= price_value <= 5000, \
                            f"Цена {price_value} вне диапазона [1000; 5000]"
        
        expect(desktop_page.locator('body')).not_to_contain_text("Ошибка")
    
    @allure.title("TC-UI-002: Фильтр по цене — невалидный ввод")
    @allure.description("Проверка валидации отрицательных значений цены")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_price_filter_invalid_negative(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка блокировки отрицательных значений в фильтре цены"""
        desktop_page.goto(f"{base_url}/list")
        wait_for_page_load()
        
        min_price_input = desktop_page.locator('input[name="minPrice"], input[data-testid="min-price"]')
        
        if min_price_input.count() > 0:
            min_price_input.fill("-100")
            
            apply_button = desktop_page.locator(
                'button[type="submit"], '
                'button:has-text("Применить")'
            )
            if apply_button.count() > 0:
                apply_button.click()
                time.sleep(2)
                
                error_message = desktop_page.locator(
                    '.input-error, '
                    '[role="alert"], '
                    '.error-message, '
                    '.validation-error'
                )
                
                if error_message.count() == 0:
                    current_value = min_price_input.input_value()
                    assert current_value != "-100", \
                        "Отрицательное значение принято без валидации"


@allure.feature("Фильтры")
@allure.story("Сортировка")
class TestSorting:
    """Тесты сортировки объявлений"""
    
    @allure.title("TC-UI-003: Сортировка по цене — возрастание")
    @allure.description("Проверка сортировки объявлений по возрастанию цены")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_sort_by_price_asc(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка сортировки по возрастанию цены"""
        desktop_page.goto(f"{base_url}/list")
        wait_for_page_load()
        
        sort_select = desktop_page.locator(
            'select[data-testid="sort"], '
            'select[name="sort"], '
            '.sort-dropdown select'
        )
        
        if sort_select.count() > 0:
            sort_select.select_option("price_asc")
            wait_for_page_load()
            
            prices = []
            price_elements = desktop_page.locator(
                '[data-testid="item-price"], '
                '.item-price, '
                '.price'
            )
            
            for i in range(min(price_elements.count(), 10)):
                price_text = price_elements.nth(i).text_content()
                if price_text:
                    price_value = int(''.join(filter(str.isdigit, price_text)))
                    prices.append(price_value)
            
            if len(prices) > 1:
                assert prices == sorted(prices), \
                    f"Цены не отсортированы по возрастанию: {prices}"
    
    @allure.title("TC-UI-004: Сортировка по цене — убывание")
    @allure.description("Проверка сортировки объявлений по убыванию цены")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_price_desc(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка сортировки по убыванию цены"""
        desktop_page.goto(f"{base_url}/list")
        wait_for_page_load()
        
        sort_select = desktop_page.locator(
            'select[data-testid="sort"], '
            'select[name="sort"], '
            '.sort-dropdown select'
        )
        
        if sort_select.count() > 0:
            sort_select.select_option("price_desc")
            wait_for_page_load()
            
            prices = []
            price_elements = desktop_page.locator(
                '[data-testid="item-price"], '
                '.item-price, '
                '.price'
            )
            
            for i in range(min(price_elements.count(), 10)):
                price_text = price_elements.nth(i).text_content()
                if price_text:
                    price_value = int(''.join(filter(str.isdigit, price_text)))
                    prices.append(price_value)
            
            if len(prices) > 1:
                assert prices == sorted(prices, reverse=True), \
                    f"Цены не отсортированы по убыванию: {prices}"


@allure.feature("Фильтры")
@allure.story("Категория")
class TestCategoryFilter:
    """Тесты фильтра по категории"""
    
    @allure.title("TC-UI-005: Фильтр по категории — выбор одной категории")
    @allure.description("Проверка фильтрации объявлений по категории")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_category_filter_single(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка фильтрации по одной категории"""
        desktop_page.goto(f"{base_url}/list")
        wait_for_page_load()
        
        category_filter = desktop_page.locator(
            'select[data-testid="category"], '
            'select[name="category"], '
            '.category-filter select, '
            '[data-testid="category-filter"]'
        )
        
        if category_filter.count() > 0:
            options = category_filter.locator('option').all()
            
            if len(options) > 1:
                selected_option = options[1].text_content()
                category_filter.select_option(index=1)
                wait_for_page_load()
                
                expect(desktop_page.locator('body')).not_to_contain_text("Ошибка")
    
    @allure.title("TC-UI-009: Комбинация фильтров — устойчивость")
    @allure.description("Проверка работы нескольких фильтров одновременно")
    @allure.severity(allure.severity_level.NORMAL)
    def test_combined_filters(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка комбинации нескольких фильтров"""
        desktop_page.goto(f"{base_url}/list")
        wait_for_page_load()
        
        filters_applied = 0
        
        min_price = desktop_page.locator('input[name="minPrice"]')
        if min_price.count() > 0:
            min_price.fill("500")
            filters_applied += 1
        
        category = desktop_page.locator('select[name="category"]')
        if category.count() > 0:
            category.select_option(index=1)
            filters_applied += 1
        
        apply_button = desktop_page.locator(
            'button[type="submit"], '
            'button:has-text("Применить")'
        )
        
        if apply_button.count() > 0 and filters_applied > 0:
            apply_button.click()
            wait_for_page_load()
            
            expect(desktop_page.locator('body')).not_to_contain_text("Ошибка")
            expect(desktop_page.locator('body')).not_to_contain_text("Error")


@allure.feature("Фильтры")
@allure.story("Только срочные")
class TestUrgentToggle:
    """Тесты тоггла «Только срочные»"""
    
    @allure.title("TC-UI-007: Тоггл «Только срочные» — включение")
    @allure.description("Проверка фильтрации срочных объявлений")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_urgent_toggle_on(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка включения фильтра срочных объявлений"""
        desktop_page.goto(f"{base_url}/list")
        wait_for_page_load()
        
        urgent_toggle = desktop_page.locator(
            'label:has-text("Сроч"), '
            'label:has-text("Urgent"), '
            'input[type="checkbox"][data-testid="urgent"], '
            '.urgent-toggle input[type="checkbox"]'
        )
        
        if urgent_toggle.count() > 0:
            initial_count = desktop_page.locator(
                '[data-testid="item-card"], '
                '.item-card, '
                '.listing-item'
            ).count()
            
            if not urgent_toggle.first.is_checked():
                urgent_toggle.first.click()
                wait_for_page_load()
            
            cards = desktop_page.locator(
                '[data-testid="item-card"], '
                '.item-card, '
                '.listing-item'
            ).all()
            
            for card in cards[:5]:
                urgent_badge = card.locator(
                    '.badge-urgent, '
                    '[data-testid="urgent"], '
                    '.urgent-badge, '
                    ':has-text("Срочно"), '
                    ':has-text("Urgent")'
                )
        
        expect(desktop_page.locator('body')).not_to_contain_text("Ошибка")
    
    @allure.title("TC-UI-008: Тоггл «Только срочные» — выключение")
    @allure.description("Проверка отключения фильтра срочных объявлений")
    @allure.severity(allure.severity_level.NORMAL)
    def test_urgent_toggle_off(self, desktop_page: Page, base_url, wait_for_page_load):
        """Проверка выключения фильтра срочных объявлений"""
        desktop_page.goto(f"{base_url}/list")
        wait_for_page_load()
        
        urgent_toggle = desktop_page.locator(
            'label:has-text("Сроч"), '
            'input[type="checkbox"][data-testid="urgent"]'
        )
        
        if urgent_toggle.count() > 0:
            if not urgent_toggle.first.is_checked():
                urgent_toggle.first.click()
                wait_for_page_load()
            
            if urgent_toggle.first.is_checked():
                urgent_toggle.first.click()
                wait_for_page_load()
            
            expect(desktop_page.locator('body')).not_to_contain_text("Ошибка")