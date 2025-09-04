from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .main_page import BasePage
from .locators import ProductPageLocators
import allure


class ProductPage(BasePage):

    def add_to_cart(self):
        with allure.step('Добавили товар в корзину'):
            add_to_cart_btn = self.browser.find_element(*ProductPageLocators.ADD_TO_CART_BUTTON)
            add_to_cart_btn.click()

    def check_product_name(self):
        with allure.step('Сравнение добавленного и реального имени товара'):
            added_prod_name = self.browser.find_element(*ProductPageLocators.NAME_OF_ADDED_PRODUCT)
            x = added_prod_name.text
            real_prod_name = self.browser.find_element(*ProductPageLocators.NAME_OF_PRODUCT)
            y = real_prod_name.text
            assert x in y, 'Неверное  имя товара'
            print('\nИмя товара проверено')

    def check_price(self):
        with allure.step('Сравнение добавленной и реальной цены товара'):
            added_prod_price = self.browser.find_element(*ProductPageLocators.PRICE_OF_ADDED_PRODUCT)
            x = added_prod_price.text
            real_prod_price = self.browser.find_element(*ProductPageLocators.PRICE_OF_PRODUCT)
            y = real_prod_price.text
            assert x == y, 'Неверная цена товара'
            print('Цена проверена')

    def go_to_cart_after_buybutton(self):
        with allure.step('Переход в корзину'):
            but = self.browser.find_element(*ProductPageLocators.MODAL_CHECKOUT)
            but.click()

    def is_buybutton_present(self):
        with allure.step('Проверка отсутствия кнопки "купить"'):
            assert self.is_not_element_present(*ProductPageLocators.ADD_TO_CART_BUTTON), \
                "Buy button is present, but should not be"

    def is_buybutton_not_present(self):
        with allure.step('Проверка наличия кнопки "купить"'):
            assert self.is_element_present(*ProductPageLocators.ADD_TO_CART_BUTTON), \
                "Buy button is not present, but should be"

    def is_buybutton_work(self):
        with allure.step('Проверка работы кнопки "купить"'):
            but = self.browser.find_element(*ProductPageLocators.ADD_TO_CART_BUTTON)
            but.click()
            assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE), \
                'Кнопка "купить не работает"'

    # noinspection PyTypeChecker
    def is_disappeared(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException).\
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

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

    def is_prodcard_open(self):
        with allure.step('Проверка открытия КТ'):
            assert self.is_element_present(*ProductPageLocators.PHOTOS), \
                "Prodcard is not opened"
            assert self.is_element_present(*ProductPageLocators.NAME_OF_PRODUCT), \
                "Prodcard is not opened"

    def photo_slider_is_present(self):
        with allure.step('Проверка наличия слайдера с фото в КТ'):
            assert self.is_not_element_present(*ProductPageLocators.PHOTOS), \
                "Photos is not presented"

    def save_product_info(self):
        with (allure.step('Запоминаем данные продукта')):
            name = self.browser.find_element(*ProductPageLocators.NAME_OF_PRODUCT).text
            variant = self.browser.find_element(*ProductPageLocators.VARIANT_OF_PRODUCT).text
            price = self.browser.find_element(*ProductPageLocators.PRICE_OF_PRODUCT).text

            return name, variant, price


    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE), \
           "Success message is presented, but should not be"
        
    def success_message_should_disappear(self):
        assert self.is_disappeared(*ProductPageLocators.SUCCESS_MESSAGE), \
           "Success message is not presented, but should be"
