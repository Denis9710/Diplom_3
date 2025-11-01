import allure
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):
    """Класс для работы с главной страницей (конструктор)"""

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = MainPageLocators

    @allure.step("Открыть главную страницу")
    def open_main_page(self, url):
        """Открыть главную страницу"""
        self.open(url)
        self.wait_for_page_load()

    @allure.step("Кликнуть на кнопку 'Конструктор'")
    def click_constructor_button(self):
        """Кликнуть на кнопку Конструктор в навигации"""
        self.click_element(self.locators.CONSTRUCTOR_BUTTON)

    @allure.step("Кликнуть на кнопку 'Лента Заказов'")
    def click_feed_button(self):
        """Кликнуть на кнопку Лента Заказов в навигации"""
        self.click_element(self.locators.FEED_BUTTON)

    @allure.step("Кликнуть на первый ингредиент (булка)")
    def click_first_ingredient(self):
        """Кликнуть на первый ингредиент для открытия модального окна"""
        self.click_element(self.locators.FIRST_BUN)

    @allure.step("Перетащить ингредиент в конструктор")
    def drag_ingredient_to_constructor(self):
        """Перетащить ингредиент в конструктор"""
        self.drag_and_drop_js(
            self.locators.FIRST_BUN,
            self.locators.DROP_TARGET,
        )

    @allure.step("Нажать кнопку 'Оформить заказ'")
    def click_order_button(self):
        """Нажать кнопку оформления заказа"""
        self.click_element(self.locators.ORDER_BUTTON)

    @allure.step("Получить значение счётчика первого ингредиента")
    def get_first_ingredient_counter(self):
        """Получить числовое значение счётчика первого ингредиента"""
        counter_text = self.get_text(self.locators.FIRST_INGREDIENT_COUNTER)
        return int(counter_text) if counter_text else 0

    @allure.step("Проверить видимость счётчика ингредиента")
    def is_ingredient_counter_visible(self):
        """Проверить, виден ли счётчик ингредиента"""
        return self.is_element_visible(self.locators.FIRST_INGREDIENT_COUNTER, timeout=5)

    @allure.step("Получить текст счётчика первого ингредиента")
    def get_first_ingredient_counter_text(self):
        """Получить текстовое значение счётчика первого ингредиента"""
        return self.get_text(self.locators.FIRST_INGREDIENT_COUNTER)

    @allure.step("Ожидать появления счётчика с нужным значением")
    def wait_for_counter_value(self, expected_value, timeout=10):
        """Ожидать появления счётчика с указанным значением"""
        return self.wait.until(
            EC.text_to_be_present_in_element(
                self.locators.FIRST_INGREDIENT_COUNTER, expected_value
            )
        )

    @allure.step("Проверить, что находимся на главной странице")
    def is_on_main_page(self):
        """Проверить, что находимся на главной странице"""
        return self.is_element_visible(self.locators.BUN_TAB)

    @allure.step("Проверить доступность кнопки заказа")
    def is_order_button_visible(self):
        """Проверить, видна ли кнопка оформления заказа"""
        return self.is_element_visible(self.locators.ORDER_BUTTON)

    @allure.step("Проверить активность кнопки заказа")
    def is_order_button_enabled(self):
        """Проверить, активна ли кнопка оформления заказа"""
        element = self.find_element(self.locators.ORDER_BUTTON)
        return element.is_enabled()

    @allure.step("Получить текст кнопки заказа")
    def get_order_button_text(self):
        """Получить текст кнопки оформления заказа"""
        return self.get_text(self.locators.ORDER_BUTTON)

    @allure.step("Дождаться доступности кнопки заказа")
    def wait_for_order_button_clickable(self, timeout=10):
        """Дождаться, пока кнопка заказа станет кликабельной"""
        return self.wait.until(
            EC.element_to_be_clickable(self.locators.ORDER_BUTTON)
        )

    @allure.step("Очистить конструктор")
    def clear_constructor(self):
        """Очистить конструктор от всех ингредиентов"""
        self.open_main_page(self.driver.current_url)

    @allure.step("Проверить наличие ингредиентов в конструкторе")
    def has_ingredients_in_constructor(self):
        """Проверить, есть ли ингредиенты в конструкторе"""
        return self.is_element_present(self.locators.DROP_TARGET)

    @allure.step("Переключиться на вкладку 'Соусы'")
    def click_sauces_tab(self):
        """Переключиться на вкладку с соусами"""
        self.click_element(self.locators.SAUCES_TAB)

    @allure.step("Переключиться на вкладку 'Начинки'")
    def click_main_tab(self):
        """Переключиться на вкладку с начинками"""
        self.click_element(self.locators.MAIN_TAB)

    @allure.step("Переключиться на вкладку 'Булки'")
    def click_bun_tab(self):
        """Переключиться на вкладку с булками"""
        self.click_element(self.locators.BUN_TAB)

    @allure.step("Получить активную вкладку")
    def get_active_tab(self):
        """Получить текст активной вкладки"""
        return self.get_text(self.locators.ACTIVE_TAB)

    @allure.step("Проверить отображение цены заказа")
    def get_order_total_price(self):
        """Получить общую стоимость заказа"""
        price_text = self.get_text(self.locators.ORDER_PRICE)
        return int(price_text) if price_text else 0

    @allure.step("Сделать скриншот главной страницы")
    def take_screenshot(self, filename="main_page_screenshot.png"):
        """Сделать скриншот главной страницы"""
        self.driver.save_screenshot(filename)
        return filename

    @allure.step("Проверить отображение логотипа")
    def is_logo_visible(self):
        """Проверить, отображается ли логотип приложения"""
        return self.is_element_visible(self.locators.LOGO)

    @allure.step("Проверить отображение личного кабинета")
    def is_profile_button_visible(self):
        """Проверить, отображается ли кнопка личного кабинета"""
        return self.is_element_visible(self.locators.PROFILE_BUTTON)

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        """Получить текущий URL страницы"""
        return self.driver.current_url

    @allure.step("Прокрутить до секции с соусами")
    def scroll_to_sauces_section(self):
        """Прокрутить страницу до секции с соусами"""
        self.scroll_to_element(self.locators.SAUCES_SECTION)

    @allure.step("Прокрутить до секции с начинками")
    def scroll_to_main_section(self):
        """Прокрутить страницу до секции с начинками"""
        self.scroll_to_element(self.locators.MAIN_SECTION)

    @allure.step("Прокрутить до секции с булками")
    def scroll_to_buns_section(self):
        """Прокрутить страницу до секции с булками"""
        self.scroll_to_element(self.locators.BUNS_SECTION)

        