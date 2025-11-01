from selenium.webdriver.common.by import By


class OrderModalLocators:
    """Локаторы элементов модального окна подтверждения заказа"""

    # Модальное окно заказа
    ORDER_MODAL = (
        By.XPATH,
        "//section[contains(@class, 'Modal_modal')]",
    )

    # Номер заказа
    ORDER_NUMBER = (
        By.XPATH,
        "//h2[contains(@class, 'Modal_modal__title')]/following-sibling::p",
    )

    # Кнопка закрытия (крестик)
    CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "section[class*='Modal_modal'] button[class*='close']",
    )
    