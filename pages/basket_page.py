import allure
from .base_page import BasePage
from .locators import BasketPageLocators
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasketPage(BasePage):
    def checkout(self):
        start = self.browser.find_element(*BasketPageLocators.CHECKOUT)
        start.click()
        phone = self.browser.find_element(*BasketPageLocators.PHONE)
        phone.send_keys('9999999999')
        buy = self.browser.find_element(*BasketPageLocators.BUY)
        buy.click()
        order = self.browser.find_element(*BasketPageLocators.ORDER_NUMBER)
        order_number = order.text
        print(' ---> ' + order_number)

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

        return False

    def items_in_basket_check(self):
        with allure.step('Проверка отображения товаров в корзине'):
            assert self.is_element_present(*BasketPageLocators.BASKET_ITEMS), "Товары в корзине"
