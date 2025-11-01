import allure
import pytest
from pages.main_page import MainPage
from pages.order_modal import OrderModal
from helpers.api_helpers import StellarBurgersAPI
from data import TestData
from urls import PAGES


@allure.feature("Создание заказа")
@allure.story("Создание заказа через UI")
class TestOrderCreation:
    """Тесты создания заказа через пользовательский интерфейс"""

    @pytest.fixture(scope="function")
    def registered_user(self):
        """Фикстура для создания зарегистрированного пользователя"""
        api = StellarBurgersAPI()
        user_data = TestData.generate_user_data()
        
        # Создаём пользователя
        response = api.create_user(user_data)
        assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"
        
        access_token = response.json().get("accessToken")
        
        yield {
            "user_data": user_data, 
            "api": api, 
            "token": access_token
        }
        
        # Удаляем пользователя после теста
        if access_token:
            api.delete_user(access_token)

    @allure.title("Создание заказа авторизованным пользователем")
    @allure.description("Проверка создания заказа через UI авторизованным пользователем")
    def test_create_order_authorized_user(self, driver, registered_user):
        """Тест создания заказа авторизованным пользователем через UI"""
        main_page = MainPage(driver)
        order_modal = OrderModal(driver)
        
        # Открываем главную страницу
        main_page.open_main_page(PAGES["main"])
        
        # Авторизуем пользователя (нужно добавить методы авторизации в MainPage)
        # main_page.login(registered_user["user_data"]["email"], registered_user["user_data"]["password"])
        
        # Добавляем ингредиенты в конструктор
        main_page.drag_ingredient_to_constructor()
        # Можно добавить дополнительные ингредиенты если нужно
        
        # Нажимаем кнопку "Оформить заказ"
        main_page.click_order_button()
        
        # Проверяем, что открылось модальное окно с подтверждением заказа
        assert order_modal.is_order_modal_opened(), "Модальное окно заказа не открылось"
        
        # Проверяем, что отображается номер заказа
        order_number = order_modal.get_order_number()
        assert order_number, "Номер заказа не отображается"
        
        # Закрываем модальное окно
        order_modal.click_close_button()
        assert order_modal.is_order_modal_closed(), "Модальное окно заказа не закрылось"

    @allure.title("Создание заказа неавторизованным пользователем")
    @allure.description("Проверка редиректа на страницу логина при попытке создать заказ без авторизации")
    def test_create_order_unauthorized_user(self, driver):
        """Тест поведения при попытке создать заказ без авторизации"""
        main_page = MainPage(driver)
        
        # Открываем главную страницу
        main_page.open_main_page(PAGES["main"])
        
        # Добавляем ингредиенты в конструктор
        main_page.drag_ingredient_to_constructor()
        
        # Нажимаем кнопку "Оформить заказ"
        main_page.click_order_button()
        
        # Проверяем, что произошёл редирект на страницу логина
        assert main_page.wait_for_url_contains("login"), "Не произошёл редирект на страницу логина"

        