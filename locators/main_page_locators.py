from selenium.webdriver.common.by import By


class MainPageLocators:
    """Локаторы элементов главной страницы"""

    # Навигация в шапке
    CONSTRUCTOR_BUTTON = (
        By.XPATH,
        "//a[@href='/' and contains(@class, 'AppHeader')]//p[text()='Конструктор']",
    )
    FEED_BUTTON = (
        By.XPATH,
        "//a[@href='/feed']//p[text()='Лента Заказов']",
    )

    # Секции конструктора (табы)
    BUN_TAB = (
        By.XPATH,
        "//span[text()='Булки']",
    )

    # Ингредиенты
    FIRST_BUN = (
        By.XPATH,
        "(//a[contains(@class, 'BurgerIngredient')])[1]",
    )

    # Конкретный счётчик первого ингредиента
    FIRST_INGREDIENT_COUNTER = (
        By.XPATH,
        "(//a[contains(@class, 'BurgerIngredient')])[1]//p[contains(@class, 'counter')]",
    )

    # Область конструктора (для перетаскивания)
    DROP_TARGET = (
        By.XPATH,
        "//section[contains(@class, 'BurgerConstructor')]",
    )

    # Кнопка оформления заказа (несколько возможных вариантов)
    ORDER_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Оформить заказ') or contains(@class, 'button_button')]",
    )
    