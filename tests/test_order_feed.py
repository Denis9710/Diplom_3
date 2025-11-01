import allure
import pytest
from pages.feed_page import FeedPage
from pages.main_page import MainPage
from helpers.api_helpers import StellarBurgersAPI
from data import TestData
from urls import PAGES


@allure.feature("Лента заказов")
@allure.story("Счётчики и отображение заказов")
class TestOrderFeed:
    """Тесты функциональности ленты заказов"""

    @pytest.fixture(scope="function")
    def user_with_order(self):
        """Фикстура для создания пользователя с заказом через UI"""
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
    def test_total_counter_increases(self, driver, user_with_order):
        """Тест увеличения общего счётчика заказов при создании нового заказа"""
        feed_page = FeedPage(driver)
        main_page = MainPage(driver)

        # Открываем страницу ленты заказов
        feed_page.open_feed_page(PAGES["feed"])

        # Получаем начальное значение счётчика
        initial_total = feed_page.get_total_orders_counter()

        # Здесь должен быть код создания заказа через UI
        # Для этого нужно:
        # 1. Авторизоваться на главной странице
        # 2. Добавить ингредиенты в конструктор
        # 3. Нажать кнопку "Оформить заказ"
        # 4. Подтвердить создание заказа
        
        # Временная заглушка - используем API для демонстрации
        # В реальном тесте это должно быть сделано через UI
        api = user_with_order["api"]
        token = user_with_order["token"]
        order_response = api.create_order_with_random_ingredients(token)
        assert order_response.status_code == 200, f"Не удалось создать заказ: {order_response.text}"

        # Получаем новое значение счётчика (обновляется автоматически)
        new_total = feed_page.get_total_orders_counter()

        # Проверяем, что счётчик увеличился
        assert new_total > initial_total, (
            f"Счётчик 'Выполнено за всё время' не увеличился. "
            f"Было: {initial_total}, стало: {new_total}"
        )

    @allure.title("Счётчик 'Выполнено за сегодня' увеличивается")
    @allure.description("Проверка увеличения счётчика заказов за текущий день")
    def test_today_counter_increases(self, driver, user_with_order):
        """Тест увеличения счётчика заказов за сегодня"""
        feed_page = FeedPage(driver)

        # Открываем страницу ленты заказов
        feed_page.open_feed_page(PAGES["feed"])

        # Получаем начальное значение счётчика
        initial_today = feed_page.get_today_orders_counter()

        # Временная заглушка - используем API для демонстрации
        api = user_with_order["api"]
        token = user_with_order["token"]
        order_response = api.create_order_with_random_ingredients(token)
        assert order_response.status_code == 200, f"Не удалось создать заказ: {order_response.text}"

        # Получаем новое значение счётчика (обновляется автоматически)
        new_today = feed_page.get_today_orders_counter()

        # Проверяем, что счётчик увеличился
        assert new_today > initial_today, (
            f"Счётчик 'Выполнено за сегодня' не увеличился. "
            f"Было: {initial_today}, стало: {new_today}"
        )

    @allure.title("Заказ появляется в ленте заказов")
    @allure.description("Проверка отображения номера заказа в ленте")
    def test_order_appears_in_progress(self, driver, user_with_order):
        """Тест отображения заказа в ленте заказов"""
        feed_page = FeedPage(driver)
        api = user_with_order["api"]
        token = user_with_order["token"]

        # Сначала открываем страницу ленты заказов
        feed_page.open_feed_page(PAGES["feed"])

        # Создаём заказ через API (временная заглушка)
        order_response = api.create_order_with_random_ingredients(token)
        assert (
            order_response.status_code == 200
        ), f"Не удалось создать заказ: {order_response.text}"

        # Получаем номер заказа
        order_number = order_response.json().get("order", {}).get("number")
        assert order_number, "Номер заказа не получен из ответа API"

        # Ожидаем появления заказа в ленте (с таймаутом 10 секунд)
        feed_page.wait_for_order_in_feed(order_number, timeout=10)

        