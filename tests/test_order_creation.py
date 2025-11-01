import allure
import pytest
from pages.main_page import MainPage
from pages.order_modal import OrderModal
from urls import PAGES


@allure.feature("Создание заказа")
@allure.story("Создание заказа через UI")
class TestOrderCreation:
    """Тесты создания заказа через пользовательский интерфейс"""

    @allure.title("Создание заказа авторизованным пользователем")
    @allure.description("Проверка создания заказа через UI авторизованным пользователем")
    def test_create_order_authorized_user(self, driver, user_with_order):
        """Тест создания заказа авторизованным пользователем через UI"""
        main_page = MainPage(driver)
        order_modal = OrderModal(driver)
        
        # Открываем главную страницу
        main_page.open_main_page(PAGES["main"])
        
        # TODO: Реализовать авторизацию через UI
        # main_page.login(user_with_order["user_data"]["email"], user_with_order["user_data"]["password"])
        
        # Добавляем ингредиенты в конструктор
        main_page.drag_ingredient_to_constructor()
        
        # Проверяем, что кнопка заказа доступна
        main_page.is_order_button_visible()
        
        # Нажимаем кнопку "Оформить заказ"
        main_page.click_order_button()
        
        # Проверяем, что открылось модальное окно с подтверждением заказа
        order_modal.is_order_modal_opened()
        
        # Проверяем, что отображается номер заказа
        order_number = order_modal.get_order_number()
        assert order_number, "Номер заказа не отображается"
        
        # Закрываем модальное окно
        order_modal.click_close_button()
        order_modal.is_order_modal_closed()

    @allure.title("Создание заказа неавторизованным пользователем")
    @allure.description("Проверка редиректа на страницу логина при попытке создать заказ без авторизации")
    def test_create_order_unauthorized_user(self, driver):
        """Тест поведения при попытке создать заказа без авторизации"""
        main_page = MainPage(driver)
        
        # Открываем главную страницу
        main_page.open_main_page(PAGES["main"])
        
        # Добавляем ингредиенты в конструктор
        main_page.drag_ingredient_to_constructor()
        
        # Проверяем, что кнопка заказа доступна
        main_page.wait_for_order_button_clickable()
        
        # Нажимаем кнопку "Оформить заказ"
        main_page.click_order_button()
        
        # Проверяем, что произошёл редирект на страницу логина
        main_page.wait_for_url_contains("login")

    @allure.title("Создание заказа с несколькими ингредиентами")
    @allure.description("Проверка создания заказа с булкой, начинкой и соусом")
    def test_create_order_with_multiple_ingredients(self, driver, user_with_order):
        """Тест создания заказа с несколькими ингредиентами"""
        main_page = MainPage(driver)
        order_modal = OrderModal(driver)
        
        # Открываем главную страницу
        main_page.open_main_page(PAGES["main"])
        
        # TODO: Реализовать авторизацию через UI
        
        # Добавляем несколько ингредиентов в конструктор
        main_page.add_multiple_ingredients_to_constructor(3)
        
        # Проверяем, что ингредиенты добавлены в конструктор
        main_page.has_ingredients_in_constructor()
        
        # Проверяем, что кнопка заказа доступна
        main_page.is_order_button_enabled()
        
        # Нажимаем кнопку "Оформить заказ"
        main_page.click_order_button()
        
        # Проверяем, что открылось модальное окно с подтверждением заказа
        order_modal.is_order_modal_opened()
        
        # Проверяем, что отображается номер заказа
        order_number = order_modal.get_order_number()
        assert order_number, "Номер заказа не отображается"
        
        # Закрываем модальное окно
        order_modal.click_close_button()
        order_modal.is_order_modal_closed()

    @allure.title("Проверка счётчика ингредиентов при создании заказа")
    @allure.description("Проверка увеличения счётчика при добавлении ингредиентов")
    def test_ingredient_counters_when_creating_order(self, driver):
        """Тест счётчиков ингредиентов при создании заказа"""
        main_page = MainPage(driver)
        
        # Открываем главную страницу
        main_page.open_main_page(PAGES["main"])
        
        # Получаем начальное значение счётчика
        initial_counter = main_page.get_first_ingredient_counter()
        
        # Добавляем ингредиент в конструктор
        main_page.drag_ingredient_to_constructor()
        
        # Ожидаем увеличения счётчика
        main_page.wait_for_counter_value("2")
        
        # Проверяем, что счётчик отображается
        main_page.is_ingredient_counter_visible()
        
        # Получаем конечное значение счётчика
        final_counter = main_page.get_first_ingredient_counter()
        
        # Проверяем, что счётчик увеличился
        assert final_counter > initial_counter, "Счётчик ингредиента не увеличился"

    @allure.title("Проверка навигации между вкладками ингредиентов")
    @allure.description("Проверка переключения между вкладками булок, соусов и начинок")
    def test_ingredient_tabs_navigation(self, driver):
        """Тест навигации по вкладкам ингредиентов"""
        main_page = MainPage(driver)
        
        # Открываем главную страницу
        main_page.open_main_page(PAGES["main"])
        
        # Проверяем, что изначально активна вкладка "Булки"
        active_tab = main_page.get_active_tab()
        assert active_tab == "Булки", f"Активна неверная вкладка: {active_tab}"
        
        # Переключаемся на вкладку "Соусы"
        main_page.click_sauces_tab()
        
        # Проверяем, что активна вкладка "Соусы"
        active_tab = main_page.get_active_tab()
        assert active_tab == "Соусы", f"Активна неверная вкладка: {active_tab}"
        
        # Переключаемся на вкладку "Начинки"
        main_page.click_main_tab()
        
        # Проверяем, что активна вкладка "Начинки"
        active_tab = main_page.get_active_tab()
        assert active_tab == "Начинки", f"Активна неверная вкладка: {active_tab}"
        
        # Возвращаемся на вкладку "Булки"
        main_page.click_bun_tab()
        
        # Проверяем, что активна вкладка "Булки"
        active_tab = main_page.get_active_tab()
        assert active_tab == "Булки", f"Активна неверная вкладка: {active_tab}"

    @allure.title("Проверка отображения цены заказа")
    @allure.description("Проверка корректного отображения общей стоимости заказа")
    def test_order_total_price_display(self, driver):
        """Тест отображения общей стоимости заказа"""
        main_page = MainPage(driver)
        
        # Открываем главную страницу
        main_page.open_main_page(PAGES["main"])
        
        # Получаем начальную цену заказа
        initial_price = main_page.get_order_total_price()
        
        # Добавляем ингредиент в конструктор
        main_page.drag_ingredient_to_constructor()
        
        # Получаем обновлённую цену заказа
        updated_price = main_page.get_order_total_price()
        
        # Проверяем, что цена увеличилась
        assert updated_price > initial_price, "Цена заказа не увеличилась после добавления ингредиента"

    @allure.title("Проверка элементов главной страницы")
    @allure.description("Проверка наличия всех основных элементов на главной странице")
    def test_main_page_elements_presence(self, driver):
        """Тест наличия основных элементов на главной странице"""
        main_page = MainPage(driver)
        
        # Открываем главную страницу
        main_page.open_main_page(PAGES["main"])
        
        # Проверяем наличие основных элементов
        main_page.is_on_main_page()
        main_page.is_logo_visible()
        main_page.is_profile_button_visible()
        main_page.is_order_button_visible()
        
        # Проверяем наличие вкладок ингредиентов
        main_page.click_bun_tab()
        main_page.click_sauces_tab()
        main_page.click_main_tab()
        
        # Возвращаемся на вкладку булок
        main_page.click_bun_tab()

    @allure.title("Проверка прокрутки к секциям ингредиентов")
    @allure.description("Проверка возможности прокрутки к разным секциям ингредиентов")
    def test_ingredient_sections_scrolling(self, driver):
        """Тест прокрутки к секциям ингредиентов"""
        main_page = MainPage(driver)
        
        # Открываем главную страницу
        main_page.open_main_page(PAGES["main"])
        
        # Прокручиваем к разным секциям
        main_page.scroll_to_buns_section()
        main_page.scroll_to_sauces_section()
        main_page.scroll_to_main_section()
        
        # Возвращаемся к секции булок
        main_page.scroll_to_buns_section()

    @allure.title("Проверка информации об ингредиентах")
    @allure.description("Проверка отображения названия и цены ингредиентов")
    def test_ingredient_info_display(self, driver):
        """Тест отображения информации об ингредиентах"""
        main_page = MainPage(driver)
        
        # Открываем главную страницу
        main_page.open_main_page(PAGES["main"])
        
        # Получаем название первого ингредиента
        ingredient_name = main_page.get_first_ingredient_name()
        assert ingredient_name, "Название ингредиента не отображается"
        
        # Получаем цену первого ингредиента
        ingredient_price = main_page.get_first_ingredient_price()
        assert ingredient_price > 0, "Цена ингредиента не отображается корректно"

        