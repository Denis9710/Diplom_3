"""Page Object для страницы ленты заказов"""

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from locators.feed_page_locators import FeedPageLocators


class FeedPage(BasePage):
    """Класс для работы со страницей ленты заказов"""

    @allure.step("Открыть страницу ленты заказов")
    def open_feed_page(self, url):
        """Открыть страницу ленты заказов"""
        self.open(url)
        self.wait_for_page_load()

    @allure.step("Проверить, что находимся на странице ленты заказов")
    def is_on_feed_page(self):
        """Проверить, что находимся на странице ленты заказов"""
        return self.is_element_visible(FeedPageLocators.FEED_TITLE)

    @allure.step("Получить значение счётчика 'Выполнено за всё время'")
    def get_total_orders_counter(self):
        """
        Получить значение счётчика выполненных заказов за всё время
        :return: число заказов
        """
        counter_text = self.get_text(FeedPageLocators.TOTAL_ORDERS_COUNTER)
        # Убираем пробелы и преобразуем в число
        return int(counter_text.replace(" ", ""))

    @allure.step("Получить значение счётчика 'Выполнено за сегодня'")
    def get_today_orders_counter(self):
        """
        Получить значение счётчика выполненных заказов за сегодня
        :return: число заказов
        """
        counter_text = self.get_text(FeedPageLocators.TODAY_ORDERS_COUNTER)
        # Убираем пробелы и преобразуем в число
        return int(counter_text.replace(" ", ""))

    @allure.step("Ожидать появления заказа в ленте")
    def wait_for_order_in_feed(self, order_number, timeout=10):
        """
        Ожидать появления заказа в ленте с таймаутом
        :param order_number: номер заказа для ожидания
        :param timeout: максимальное время ожидания в секундах
        """
        # Форматируем номер заказа до 6 символов с ведущими нулями
        order_formatted = str(order_number).zfill(6)

        def order_is_present(driver):
            """Проверяет наличие заказа с форматированным номером"""
            template = FeedPageLocators.ORDER_NUMBER_TEMPLATE
            locator = (By.XPATH, template.format(order_formatted))
            return self.is_element_visible(locator, timeout=1)

        return self.wait_for_custom_condition(
            order_is_present, 
            timeout=timeout,
            poll_frequency=0.5
        )
    
    