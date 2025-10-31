"""Конфигурация pytest и фикстуры для тестов"""

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class DriverFactory:
    """Фабрика для создания драйверов браузеров"""

    @staticmethod
    def create_chrome_driver():
        """Создание Chrome драйвера с настройками"""
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )
        return driver

    @staticmethod
    def create_firefox_driver():
        """Создание Firefox драйвера с настройками"""
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
        )
        return driver

    @staticmethod
    def get_driver(browser_name):
        """
        Получение драйвера по имени браузера
        :param browser_name: название браузера (chrome, firefox)
        :return: WebDriver instance
        """
        drivers = {
            "chrome": DriverFactory.create_chrome_driver,
            "firefox": DriverFactory.create_firefox_driver,
        }

        driver_creator = drivers.get(browser_name.lower())
        if not driver_creator:
            raise ValueError(
                f"Браузер '{browser_name}' не поддерживается. "
                f"Доступные браузеры: {', '.join(drivers.keys())}"
            )

        return driver_creator()


def pytest_addoption(parser):
    """Добавление опции командной строки для выбора браузера"""
    parser.addoption(
        "--browser-name",
        action="store",
        default="chrome",
        help="Выбор браузера: chrome или firefox",
    )


@pytest.fixture(scope="function")
def browser_name(request):
    """Фикстура для получения имени браузера из командной строки"""
    return request.config.getoption("--browser-name")


@pytest.fixture(scope="function")
def driver(request, browser_name):
    """Фикстура для создания и закрытия WebDriver"""
    # Добавляем информацию о браузере в Allure отчёт
    allure.dynamic.parameter("Browser", browser_name.upper())

    # Создаем драйвер через фабрику
    driver = DriverFactory.get_driver(browser_name)

    driver.implicitly_wait(10)
    driver.maximize_window()

    yield driver

    # Сделать скриншот при падении теста
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG,
        )

    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для сохранения результата выполнения теста"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def drag_and_drop_js():
    """
    JavaScript функция для drag-and-drop.
    Необходима для корректной работы в Firefox.
    """
    return """
    function simulateDragDrop(sourceNode, destinationNode) {
        var EVENT_TYPES = {
            DRAG_END: 'dragend',
            DRAG_START: 'dragstart',
            DROP: 'drop'
        }

        function createCustomEvent(type) {
            var event = new CustomEvent("CustomEvent")
            event.initCustomEvent(type, true, true, null)
            event.dataTransfer = {
                data: {
                },
                setData: function(type, val) {
                    this.data[type] = val
                },
                getData: function(type) {
                    return this.data[type]
                }
            }
            return event
        }

        function dispatchEvent(node, type, event) {
            if (node.dispatchEvent) {
                return node.dispatchEvent(event)
            }
            if (node.fireEvent) {
                return node.fireEvent("on" + type, event)
            }
        }

        var event = createCustomEvent(EVENT_TYPES.DRAG_START)
        dispatchEvent(sourceNode, EVENT_TYPES.DRAG_START, event)

        var dropEvent = createCustomEvent(EVENT_TYPES.DROP)
        dropEvent.dataTransfer = event.dataTransfer
        dispatchEvent(destinationNode, EVENT_TYPES.DROP, dropEvent)

        var dragEndEvent = createCustomEvent(EVENT_TYPES.DRAG_END)
        dragEndEvent.dataTransfer = event.dataTransfer
        dispatchEvent(sourceNode, EVENT_TYPES.DRAG_END, dragEndEvent)
    }

    simulateDragDrop(arguments[0], arguments[1]);
    """
