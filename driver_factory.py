"""Фабрика для создания драйверов браузеров"""

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
    