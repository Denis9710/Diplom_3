import allure
import pytest
from pages.main_page import MainPage
from pages.feed_page import FeedPage
from helpers.api_helpers import StellarBurgersAPI
from data import TestData
from urls import PAGES


@allure.feature("Лента заказов")
@allure.story("Счётчики и отображение заказов")
class TestOrderFeed:
    """Тесты функциональности ленты заказов"""

    @pytest.fixture(scope="function")
    def user_with_order(self):
        """
        Фикстура создания пользователя через API
        :return: данные пользователя и API клиент
        """
        api = StellarBurgersAPI()

        # Генерируем данные пользователя
        user_data = TestData.generate_user_data()

        # Создаём пользователя
        response = api.create_user(user_data)
        assert (
            response.status_code == 200
        ), f"Не удалось создать пользователя: {response.text}"

        # Получаем токен
        access_token = response.json().get("accessToken")

        yield {"user_data": user_data, "api": api, "token": access_token}

        # Удаляем пользователя после теста
        if access_token:
            api.delete_user(access_token)

    @allure.title("Счётчик 'Выполнено за всё время' увеличивается")
    @allure.description("Проверка увеличения счётчика общего количества заказов")
    def test_total_counter_increases(self, driver, user_with_order, drag_and_drop_js):
        """
        Тест проверяет увеличение счётчика 'Выполнено за всё время'
        1. Открываем главную страницу и логинимся
        2. Открываем ленту заказов и получаем начальное значение счётчика
        3. Создаём новый заказ через UI
        4. Проверяем, что счётчик увеличился
        """
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)

        # Открываем главную страницу и логинимся
        main_page.open_main_page(PAGES["main"])
        main_page.login(
            user_with_order["user_data"]["email"], 
            user_with_order["user_data"]["password"]
        )

        # Открываем страницу ленты заказов и получаем начальное значение
        feed_page.open_feed_page(PAGES["feed"])
        initial_total = feed_page.get_total_orders_counter()

        # Возвращаемся на главную и создаём заказ через UI
        main_page.open_main_page(PAGES["main"])
        order_number = main_page.create_order_ui(drag_and_drop_js)
        
        assert order_number is not None, "Не удалось создать заказ через UI"

        # Ждём обновления данных (может потребоваться время)
        main_page.wait_explicitly(3)

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
    def test_today_counter_increases(self, driver, user_with_order, drag_and_drop_js):
        """
        Тест проверяет увеличение счётчика 'Выполнено за сегодня'
        1. Открываем главную страницу и логинимся
        2. Открываем ленту заказов и получаем начальное значение счётчика
        3. Создаём новый заказ через UI
        4. Проверяем, что счётчик увеличился
        """
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)

        # Открываем главную страницу и логинимся
        main_page.open_main_page(PAGES["main"])
        main_page.login(
            user_with_order["user_data"]["email"], 
            user_with_order["user_data"]["password"]
        )

        # Открываем страницу ленты заказов и получаем начальное значение
        feed_page.open_feed_page(PAGES["feed"])
        initial_today = feed_page.get_today_orders_counter()

        # Возвращаемся на главную и создаём заказ через UI
        main_page.open_main_page(PAGES["main"])
        order_number = main_page.create_order_ui(drag_and_drop_js)
        
        assert order_number is not None, "Не удалось создать заказ через UI"

        # Ждём обновления данных
        main_page.wait_explicitly(3)

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
    def test_order_appears_in_progress(self, driver, user_with_order, drag_and_drop_js):
        """
        Тест проверяет появление заказа в ленте заказов
        1. Открываем главную страницу и логинимся
        2. Создаём заказ через UI
        3. Ожидаем появления заказа в ленте
        4. Проверяем, что заказ появился в ленте
        """
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)

        # Открываем главную страницу и логинимся
        main_page.open_main_page(PAGES["main"])
        main_page.login(
            user_with_order["user_data"]["email"], 
            user_with_order["user_data"]["password"]
        )

        # Создаём заказ через UI
        order_number = main_page.create_order_ui(drag_and_drop_js)
        assert order_number is not None, "Не удалось создать заказ через UI"

        # Ждём обновления данных
        main_page.wait_explicitly(3)

        # Открываем ленту заказов и проверяем наличие заказа
        feed_page.open_feed_page(PAGES["feed"])
        
        # Ожидаем появления заказа в ленте
        feed_page.wait_for_order_in_feed(order_number, timeout=10)

