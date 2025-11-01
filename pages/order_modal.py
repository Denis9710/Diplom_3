import allure
from pages.base_page import BasePage
from locators.order_modal_locators import OrderModalLocators


class OrderModal(BasePage):
    """Класс для работы с модальным окном подтверждения заказа"""

    @allure.step("Проверить, что модальное окно заказа открыто")
    def is_order_modal_opened(self):
        """Проверить, что модальное окно заказа открыто"""
        return self.is_element_visible(OrderModalLocators.ORDER_MODAL)

    @allure.step("Проверить, что модальное окно заказа закрыто")
    def is_order_modal_closed(self):
        """Проверить, что модальное окно заказа закрыто"""
        return self.wait_for_element_to_disappear(OrderModalLocators.ORDER_MODAL)

    @allure.step("Получить номер заказа")
    def get_order_number(self):
        """Получить номер созданного заказа"""
        return self.get_text(OrderModalLocators.ORDER_NUMBER)

    @allure.step("Кликнуть на кнопку закрытия")
    def click_close_button(self):
        """Закрыть модальное окно заказа"""
        self.click_element(OrderModalLocators.CLOSE_BUTTON)

        