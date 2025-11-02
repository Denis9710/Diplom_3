"""Page Object для главной страницы (конструктор)"""

import allure
import time
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
    def drag_ingredient_to_constructor(self, drag_and_drop_script):
        """
        Перетащить первый ингредиент в конструктор
        :param drag_and_drop_script: JavaScript для drag and drop
        """
        self.drag_and_drop_js(
            MainPageLocators.FIRST_BUN,
            MainPageLocators.DROP_TARGET,
            drag_and_drop_script,
        )

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
        """
        self.wait_for_text_in_element(
            MainPageLocators.FIRST_INGREDIENT_COUNTER, expected_value, timeout
        )

    @allure.step("Проверить, что находимся на главной странице")
    def is_on_main_page(self):
        """Проверить, что находимся на главной странице"""
        return self.is_element_visible(MainPageLocators.BUN_TAB)

    @allure.step("Авторизоваться пользователем")
    def login(self, email, password):
        """Авторизация пользователя через UI"""
        # Клик на кнопку "Войти в аккаунт" на главной
        self.click_element(MainPageLocators.LOGIN_BUTTON)
        
        # Ожидание загрузки страницы логина
        self.wait_for_page_load()
        
        # Ввод email
        self.input_text(MainPageLocators.EMAIL_INPUT, email)
        
        # Ввод пароля
        self.input_text(MainPageLocators.PASSWORD_INPUT, password)
        
        # Клик на кнопку входа
        self.click_element(MainPageLocators.LOGIN_SUBMIT_BUTTON)
        
        # Ожидание возврата на главную страницу и появления кнопки "Оформить заказ"
        self.wait_for_custom_condition(
            lambda d: self.is_element_visible(MainPageLocators.AUTH_SUCCESS_INDICATOR),
            timeout=10
        )
        
        # Дополнительное ожидание полной загрузки
        self.wait_for_page_load()

    @allure.step("Проверить, что пользователь авторизован")
    def is_user_logged_in(self):
        """Проверить, что пользователь авторизован (видна кнопка Оформить заказ)"""
        return self.is_element_visible(MainPageLocators.AUTH_SUCCESS_INDICATOR)

    @allure.step("Создать заказ через UI")
    def create_order_ui(self, drag_and_drop_script):
        """
        Создать заказ через пользовательский интерфейс
        1. Добавить булку в конструктор
        2. Добавить соус в конструктор
        3. Добавить начинку в конструктор
        4. Нажать кнопку "Оформить заказ"
        :param drag_and_drop_script: JavaScript для drag and drop
        :return: номер созданного заказа
        """
        # Проверяем, что пользователь авторизован
        if not self.is_user_logged_in():
            raise Exception("Пользователь не авторизован для создания заказа")

        # Добавляем булку
        self.drag_and_drop_js(
            MainPageLocators.FIRST_BUN,
            MainPageLocators.DROP_TARGET,
            drag_and_drop_script,
        )

        # Добавляем соус
        self.drag_and_drop_js(
            MainPageLocators.FIRST_SAUCE,
            MainPageLocators.DROP_TARGET,
            drag_and_drop_script,
        )

        # Добавляем начинку
        self.drag_and_drop_js(
            MainPageLocators.FIRST_MAIN,
            MainPageLocators.DROP_TARGET,
            drag_and_drop_script,
        )

        # Проверяем, что кнопка стала активной
        self.wait_for_custom_condition(
            lambda d: self.is_element_visible(MainPageLocators.CREATE_ORDER_BUTTON),
            timeout=5
        )

        # Нажимаем кнопку "Оформить заказ"
        self.click_element(MainPageLocators.CREATE_ORDER_BUTTON)

        # Ожидаем появления модального окна с номером заказа
        self.wait_for_order_modal()

        # Получаем номер заказа
        order_number = self.get_order_number_from_modal()
        
        # Закрываем модальное окно после получения номера
        self.click_element(MainPageLocators.CLOSE_ORDER_MODAL)
        
        return order_number

    @allure.step("Ожидать появления модального окна заказа")
    def wait_for_order_modal(self, timeout=10):
        """Ожидать появления модального окна с деталями заказа"""
        return self.wait_for_custom_condition(
            lambda d: self.is_element_visible(MainPageLocators.ORDER_MODAL),
            timeout=timeout
        )

    @allure.step("Получить номер заказа из модального окна")
    def get_order_number_from_modal(self):
        """Получить номер созданного заказа из модального окна"""
        order_text = self.get_text(MainPageLocators.ORDER_NUMBER)
        # Извлекаем только цифры из текста
        import re
        numbers = re.findall(r'\d+', order_text)
        return int(numbers[0]) if numbers else None

    @allure.step("Явное ожидание {seconds} секунд")
    def wait_explicitly(self, seconds):
        """Явное ожидание (использовать только когда необходимо)"""
        time.sleep(seconds)
        