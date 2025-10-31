"""Локаторы для страницы ленты заказов"""

from selenium.webdriver.common.by import By


class FeedPageLocators:
    """Локаторы элементов страницы ленты заказов"""

    # Заголовок страницы
    FEED_TITLE = (
        By.XPATH,
        "//h1[text()='Лента заказов']",
    )

    # Счётчики
    TOTAL_ORDERS_COUNTER = (
        By.XPATH,
        "//p[text()='Выполнено за все время:']/following-sibling::p",
    )
    TODAY_ORDERS_COUNTER = (
        By.XPATH,
        "//p[text()='Выполнено за сегодня:']/following-sibling::p",
    )

    # Номер заказа в списке заказов
    ORDER_NUMBER_TEMPLATE = "//p[text()='#{}']"
