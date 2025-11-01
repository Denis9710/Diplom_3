"""Тесты ленты заказов Stellar Burgers"""

import allure
import pytest
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
        Фикстура создания пользователя и заказа через API
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
    def test_total_counter_increases(self, driver, user_with_order):
        """
        Тест проверяет увеличение счётчика 'Выполнено за всё время'
        1. Открываем страницу ленты заказов
        2. Получаем текущее значение счётчика
        3. Создаём новый заказ через API
        4. Обновляем страницу
        5. Проверяем, что счётчик увеличился
        """
        feed_page = FeedPage(driver)
        api = user_with_order["api"]
        token = user_with_order["token"]

        # Открываем страницу ленты заказов
        feed_page.open_feed_page(PAGES["feed"])

        # Получаем начальное значение счётчика
        initial_total = feed_page.get_total_orders_counter()

        # Создаём заказ через API
        order_response = api.create_order_with_random_ingredients(token)
        assert (
            order_response.status_code == 200
        ), f"Не удалось создать заказ: {order_response.text}"

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
        """
        Тест проверяет увеличение счётчика 'Выполнено за сегодня'
        1. Открываем страницу ленты заказов
        2. Получаем текущее значение счётчика
        3. Создаём новый заказ через API
        4. Обновляем страницу
        5. Проверяем, что счётчик увеличился
        """
        feed_page = FeedPage(driver)
        api = user_with_order["api"]
        token = user_with_order["token"]

        # Открываем страницу ленты заказов
        feed_page.open_feed_page(PAGES["feed"])

        # Получаем начальное значение счётчика
        initial_today = feed_page.get_today_orders_counter()

        # Создаём заказ через API
        order_response = api.create_order_with_random_ingredients(token)
        assert (
            order_response.status_code == 200
        ), f"Не удалось создать заказ: {order_response.text}"

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
        """
        Тест проверяет появление заказа в ленте заказов
        1. Открываем страницу ленты заказов
        2. Создаём заказ через API
        3. Ожидаем появления заказа в ленте (до 10 секунд)
        4. Проверяем, что заказ появился в ленте
        """
        feed_page = FeedPage(driver)
        api = user_with_order["api"]
        token = user_with_order["token"]

        # Сначала открываем страницу ленты заказов
        feed_page.open_feed_page(PAGES["feed"])

        # Создаём заказ через API
        order_response = api.create_order_with_random_ingredients(token)
        assert (
            order_response.status_code == 200
        ), f"Не удалось создать заказ: {order_response.text}"

        # Получаем номер заказа
        order_number = order_response.json().get("order", {}).get("number")
        assert order_number, "Номер заказа не получен из ответа API"

        # Ожидаем появления заказа в ленте (с таймаутом 10 секунд)
        feed_page.wait_for_order_in_feed(order_number, timeout=10)
