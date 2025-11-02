import allure
import pytest
from pages.feed_page import FeedPage
from pages.main_page import MainPage
from urls import PAGES


@allure.feature("Лента заказов")
@allure.story("Счётчики и отображение заказов")
class TestOrderFeed:
    """Тесты функциональности ленты заказов"""

    @allure.title("Счётчик 'Выполнено за всё время' увеличивается")
    @allure.description("Проверка увеличения счётчика общего количества заказов")
    def test_total_counter_increases(self, driver, logged_in_user):
        """
        Тест проверяет увеличение счётчика 'Выполнено за всё время'
        1. Открываем страницу ленты заказов
        2. Получаем текущее значение счётчика
        3. Создаём новый заказ через UI
        4. Проверяем, что счётчик увеличился
        """
        feed_page = FeedPage(driver)
        main_page = MainPage(driver)

        # Открываем страницу ленты заказов
        feed_page.open_feed_page(PAGES["feed"])

        # Получаем начальное значение счётчика
        initial_total = feed_page.get_total_orders_counter()

        # Создаём заказ через UI
        main_page.open_main_page(PAGES["main"])
        
        # Добавляем полный набор ингредиентов
        main_page.add_full_ingredients_set()
        
        main_page.create_order()
        main_page.wait_for_order_created()
        main_page.close_order_modal()

        # Возвращаемся на ленту заказов и проверяем счётчик
        feed_page.open_feed_page(PAGES["feed"])
        new_total = feed_page.get_total_orders_counter()

        # Проверяем, что счётчик увеличился
        assert new_total > initial_total, (
            f"Счётчик 'Выполнено за всё время' не увеличился. "
            f"Было: {initial_total}, стало: {new_total}"
        )

    @allure.title("Счётчик 'Выполнено за сегодня' увеличивается")
    @allure.description("Проверка увеличения счётчика заказов за текущий день")
    def test_today_counter_increases(self, driver, logged_in_user):
        """
        Тест проверяет увеличение счётчика 'Выполнено за сегодня'
        1. Открываем страницу ленты заказов
        2. Получаем текущее значение счётчика
        3. Создаём новый заказ через UI
        4. Проверяем, что счётчик увеличился
        """
        feed_page = FeedPage(driver)
        main_page = MainPage(driver)

        # Открываем страницу ленты заказов
        feed_page.open_feed_page(PAGES["feed"])

        # Получаем начальное значение счётчика
        initial_today = feed_page.get_today_orders_counter()

        # Создаём заказ через UI
        main_page.open_main_page(PAGES["main"])
        
        # Добавляем полный набор ингредиентов
        main_page.add_full_ingredients_set()
        
        main_page.create_order()
        main_page.wait_for_order_created()
        main_page.close_order_modal()

        # Возвращаемся на ленту заказов и проверяем счётчик
        feed_page.open_feed_page(PAGES["feed"])
        new_today = feed_page.get_today_orders_counter()

        # Проверяем, что счётчик увеличился
        assert new_today > initial_today, (
            f"Счётчик 'Выполнено за сегодня' не увеличился. "
            f"Было: {initial_today}, стало: {new_today}"
        )

    @allure.title("Заказ появляется в ленте заказов")
    @allure.description("Проверка отображения номера заказа в ленте")
    def test_order_appears_in_progress(self, driver, logged_in_user):
        """
        Тест проверяет появление заказа в ленте заказов
        1. Открываем страницу ленты заказов
        2. Создаём заказ через UI
        3. Ожидаем появления заказа в ленте
        4. Проверяем, что заказ появился в ленте
        """
        feed_page = FeedPage(driver)
        main_page = MainPage(driver)

        # Сначала открываем страницу ленты заказов для получения начального состояния
        feed_page.open_feed_page(PAGES["feed"])

        # Создаём заказ через UI
        main_page.open_main_page(PAGES["main"])
        
        # Добавляем полный набор ингредиентов
        main_page.add_full_ingredients_set()
        
        main_page.create_order()
        order_number = main_page.get_order_number()
        main_page.close_order_modal()

        # Проверяем появление заказа в ленте
        feed_page.open_feed_page(PAGES["feed"])
        assert feed_page.wait_for_order_in_feed(order_number, timeout=15), (
            f"Заказ #{order_number} не появился в ленте заказов"
        )

        