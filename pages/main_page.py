import allure
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):
    """Класс для работы с главной страницей (конструктор)"""

    @allure.step("Открыть главную страницу")
    def open_main_page(self, url):
        """Открыть главную страницу"""
        self.open(url)
        self.wait_for_page_load()

    @allure.step("Кликнуть на кнопку 'Конструктор'")
    def click_constructor_button(self):
        """Кликнуть на кнопку Конструктор в навигации"""
        self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)

    @allure.step("Кликнуть на кнопку 'Лента Заказов'")
    def click_feed_button(self):
        """Кликнуть на кнопку Лента Заказов в навигации"""
        self.click_element(MainPageLocators.FEED_BUTTON)

    @allure.step("Кликнуть на первый ингредиент (булка)")
    def click_first_ingredient(self):
        """Кликнуть на первый ингредиент для открытия модального окна"""
        self.click_element(MainPageLocators.FIRST_BUN)

    @allure.step("Перетащить ингредиент в конструктор")
    def drag_ingredient_to_constructor(self):
        """Перетащить ингредиент в конструктор"""
        self.drag_and_drop_js(
            MainPageLocators.FIRST_BUN,
            MainPageLocators.DROP_TARGET,
        )

    @allure.step("Получить значение счётчика первого ингредиента")
    def get_first_ingredient_counter(self):
        """Получить числовое значение счётчика первого ингредиента"""
        if self.is_element_visible(
            MainPageLocators.FIRST_INGREDIENT_COUNTER, timeout=2
        ):
            counter_text = self.get_text(MainPageLocators.FIRST_INGREDIENT_COUNTER)
            return int(counter_text) if counter_text else 0
        return 0

    @allure.step("Проверить видимость счётчика ингредиента")
    def is_ingredient_counter_visible(self):
        """Проверить, виден ли счётчик ингредиента"""
        return self.is_element_visible(
            MainPageLocators.FIRST_INGREDIENT_COUNTER, timeout=5
        )

    @allure.step("Получить текст счётчика первого ингредиента")
    def get_first_ingredient_counter_text(self):
        """Получить текстовое значение счётчика первого ингредиента"""
        return self.get_text(MainPageLocators.FIRST_INGREDIENT_COUNTER)

    @allure.step("Ожидать появления счётчика с нужным значением")
    def wait_for_counter_value(self, expected_value, timeout=10):
        """Ожидать появления счётчика с указанным значением"""
        from selenium.webdriver.support import expected_conditions as EC
        
        return WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(
                MainPageLocators.FIRST_INGREDIENT_COUNTER, expected_value
            )
        )

    @allure.step("Проверить, что находимся на главной странице")
    def is_on_main_page(self):
        """Проверить, что находимся на главной странице"""
        # Проверяем наличие таба "Булки" - он всегда есть на главной
        return self.is_element_visible(MainPageLocators.BUN_TAB)
    
    