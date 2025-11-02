import allure
import re
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):
    """Класс для работы с главной страницей (конструктор)"""

    @allure.step("Открыть главную страницу")
    def open_main_page(self, url):
        """Открыть главную страницу"""
        self.open(url)
        self.wait_for_page_load()

    @allure.step("Перетащить ингредиент в конструктор")
    def drag_ingredient_to_constructor(self):
        """Перетащить первый ингредиент в конструктор"""
        self.drag_and_drop_js(
            MainPageLocators.FIRST_BUN,
            MainPageLocators.DROP_TARGET
        )

    @allure.step("Создать заказ")
    def create_order(self):
        """Создать заказ"""
        self.click_element(MainPageLocators.CREATE_ORDER_BUTTON)

    @allure.step("Ожидать создания заказа")
    def wait_for_order_created(self, timeout=15):
        """Ожидать завершения создания заказа"""
        return self.wait_for_element_visible(MainPageLocators.ORDER_MODAL, timeout)

    @allure.step("Получить номер заказа")
    def get_order_number(self):
        """Получить номер созданного заказа"""
        order_text = self.get_text(MainPageLocators.ORDER_NUMBER)
        # Извлекаем только цифры из текста
        numbers = re.findall(r'\d+', order_text)
        return numbers[0] if numbers else None

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        """Закрыть модальное окно с информацией о заказе"""
        self.click_element(MainPageLocators.CLOSE_ORDER_BUTTON)

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

    @allure.step("Получить значение счётчика первого ингредиента")
    def get_first_ingredient_counter(self):
        """
        Получить значение счётчика первого ингредиента
        :return: значение счётчика или 0 если счётчик не виден
        """
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
        """
        Получить текст счётчика первого ингредиента как строку
        :return: текст счётчика
        """
        return self.get_text(MainPageLocators.FIRST_INGREDIENT_COUNTER)

    @allure.step("Ожидать появления счётчика с нужным значением")
    def wait_for_counter_value(self, expected_value, timeout=10):
        """
        Ожидать, что счётчик ингредиента примет нужное значение
        :param expected_value: ожидаемое значение счётчика (строка)
        :param timeout: максимальное время ожидания в секундах
        :return: True если счётчик достиг нужного значения
        """
        return self.wait_for_text_in_element(
            MainPageLocators.FIRST_INGREDIENT_COUNTER, expected_value, timeout
        )

    @allure.step("Проверить, что находимся на главной странице")
    def is_on_main_page(self):
        """Проверить, что находимся на главной странице"""
        return self.is_element_visible(MainPageLocators.BUN_TAB)
    

