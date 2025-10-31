"""Базовый класс для всех страниц"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class BasePage:
    """Базовый класс для всех Page Object классов"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть URL: {url}")
    def open(self, url):
        """Открыть страницу по URL"""
        self.driver.get(url)

    @allure.step("Найти элемент с локатором: {locator}")
    def find_element(self, locator, timeout=10):
        """Найти элемент с ожиданием"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Найти все элементы с локатором: {locator}")
    def find_elements(self, locator, timeout=10):
        """Найти все элементы с ожиданием"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return self.driver.find_elements(*locator)

    @allure.step("Кликнуть по элементу")
    def click_element(self, locator, timeout=10):
        """Кликнуть по элементу с ожиданием"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    @allure.step("Ввести текст '{text}' в поле")
    def input_text(self, locator, text, timeout=10):
        """Ввести текст в поле"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента")
    def get_text(self, locator, timeout=10):
        """Получить текст элемента"""
        element = self.find_element(locator, timeout)
        return element.text

    @allure.step("Проверить видимость элемента")
    def is_element_visible(self, locator, timeout=3):
        """Проверить видимость элемента"""
        elements = self.driver.find_elements(*locator)
        return len(elements) > 0 and elements[0].is_displayed()

    @allure.step("Проверить наличие элемента")
    def is_element_present(self, locator, timeout=3):
        """Проверить наличие элемента на странице"""
        elements = self.driver.find_elements(*locator)
        return len(elements) > 0

    @allure.step("Ждать исчезновения элемента")
    def wait_for_element_to_disappear(self, locator, timeout=10):
        """Ждать исчезновения элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    @allure.step("Скроллить до элемента")
    def scroll_to_element(self, locator):
        """Скроллить до элемента"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        """Получить текущий URL"""
        return self.driver.current_url

    @allure.step("Ждать изменения URL")
    def wait_for_url_change(self, expected_url, timeout=10):
        """Ждать изменения URL на ожидаемый"""
        return WebDriverWait(self.driver, timeout).until(EC.url_to_be(expected_url))

    @allure.step("Ждать, что URL содержит текст")
    def wait_for_url_contains(self, text, timeout=10):
        """Ждать, что URL содержит определенный текст"""
        return WebDriverWait(self.driver, timeout).until(EC.url_contains(text))

    @allure.step("Выполнить drag and drop через JavaScript")
    def drag_and_drop_js(self, source_locator, target_locator, js_script):
        """
        Выполнить drag and drop с использованием JavaScript
        Необходимо для корректной работы в Firefox
        :param source_locator: локатор элемента источника
        :param target_locator: локатор элемента назначения
        :param js_script: JavaScript код для drag and drop
        """
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)
        self.driver.execute_script(js_script, source, target)

    @allure.step("Получить значение атрибута элемента")
    def get_attribute(self, locator, attribute_name, timeout=10):
        """Получить значение атрибута элемента"""
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute_name)

    @allure.step("Ждать загрузки страницы")
    def wait_for_page_load(self, timeout=10):
        """Ждать полной загрузки страницы"""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
