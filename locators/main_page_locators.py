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
        "//span[text()='Булки']/parent::div",
    )
    SAUCES_TAB = (
        By.XPATH, 
        "//span[text()='Соусы']/parent::div",
    )
    MAIN_TAB = (
        By.XPATH,
        "//span[text()='Начинки']/parent::div",
    )

    # Ингредиенты
    FIRST_BUN = (
        By.XPATH,
        "(//div[contains(@class, 'BurgerIngredient_ingredient')])[1]",
    )

    # Конкретный счётчик первого ингредиента
    FIRST_INGREDIENT_COUNTER = (
        By.XPATH,
        "(//div[contains(@class, 'BurgerIngredient_ingredient')])[1]//p[contains(@class, 'counter')]",
    )

    # Область конструктора (для перетаскивания)
    DROP_TARGET = (
        By.XPATH,
        "//section[contains(@class, 'BurgerConstructor_basket')]",
    )

    # Кнопка оформления заказа
    ORDER_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Оформить заказ')]",
    )

    # Логотип
    LOGO = (
        By.XPATH,
        "//div[contains(@class, 'AppHeader_header__logo')]",
    )

    # Кнопка личного кабинета
    PROFILE_BUTTON = (
        By.XPATH,
        "//a[contains(@href, '/profile')]",
    )

    # Активная вкладка
    ACTIVE_TAB = (
        By.XPATH,
        "//div[contains(@class, 'tab_tab_type_current')]",
    )

    # Цена заказа
    ORDER_PRICE = (
        By.XPATH,
        "//p[contains(@class, 'OrderTotal')]",
    )

    # Название ингредиента
    INGREDIENT_NAME = (
        By.XPATH,
        "(//div[contains(@class, 'BurgerIngredient_ingredient')])[1]//p[contains(@class, 'text_type_main-default')]",
    )

    # Цена ингредиента
    INGREDIENT_PRICE = (
        By.XPATH,
        "(//div[contains(@class, 'BurgerIngredient_ingredient')])[1]//p[contains(@class, 'text_type_digits-default')]",
    )

    # Секции ингредиентов
    BUNS_SECTION = (
        By.XPATH,
        "//h2[text()='Булки']",
    )
    SAUCES_SECTION = (
        By.XPATH,
        "//h2[text()='Соусы']",
    )
    MAIN_SECTION = (
        By.XPATH,
        "//h2[text()='Начинки']",
    )

    