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
    SAUCES_TAB = (
        By.XPATH,
        "//span[text()='Соусы']",
    )
    FILLINGS_TAB = (
        By.XPATH,
        "//span[text()='Начинки']",
    )

    # Ингредиенты - булки
    FIRST_BUN = (
        By.XPATH,
        "(//a[contains(@class, 'BurgerIngredient')])[1]",
    )
    BUN_SECTION = (
        By.XPATH,
        "//h2[text()='Булки']/following-sibling::ul",
    )

    # Ингредиенты - соусы
    SAUCES_SECTION = (
        By.XPATH,
        "//h2[text()='Соусы']/following-sibling::ul",
    )
    FIRST_SAUCE = (
        By.XPATH,
        "//h2[text()='Соусы']/following-sibling::ul//a[contains(@class, 'BurgerIngredient')][1]",
    )

    # Ингредиенты - начинки
    FILLINGS_SECTION = (
        By.XPATH,
        "//h2[text()='Начинки']/following-sibling::ul",
    )
    FIRST_FILLING = (
        By.XPATH,
        "//h2[text()='Начинки']/following-sibling::ul//a[contains(@class, 'BurgerIngredient')][1]",
    )

    # Конкретный счётчик первого ингредиента
    FIRST_INGREDIENT_COUNTER = (
        By.XPATH,
        "(//a[contains(@class, 'BurgerIngredient')])[1]"
        "//p[@class='counter_counter__num__3nue1']",
    )

    # Область конструктора (для перетаскивания)
    DROP_TARGET = (
        By.XPATH,
        "//section[contains(@class, 'BurgerConstructor')]",
    )

    # Кнопка создания заказа
    CREATE_ORDER_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Оформить заказ')]",
    )

    # Модальное окно заказа
    ORDER_MODAL = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal')]//h2[contains(text(), 'идентификатор заказа')]",
    )

    ORDER_NUMBER = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal')]//h2[contains(@class, 'Modal_modal__title')]",
    )

    CLOSE_ORDER_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal')]//button[contains(@class, 'Modal_modal__close')]",
    )

    