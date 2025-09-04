from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .locators import BasePageLocators
import allure


class BasePage:
    def basket_is_empty(self): # корзина должна быть пуста
        with allure.step('Корзина пуста'):
            assert self.is_disappeared(*BasePageLocators.BASKET_COUNT), "Корзина не пуста"

    def basket_is_not_empty(self): # корзина должна быть не пуста
        with allure.step('Корзина не пуста'):
            assert self.is_not_element_present(*BasePageLocators.BASKET_COUNT), "Корзина пуста"

    def go_to_basket_page(self):
        with allure.step('Переход в корзину'):
            go = self.browser.find_element(*BasePageLocators.BASKET_LINK)
            go.click()

    def go_to_category1(self):
        with allure.step('Переход в каталог'):
            go = self.browser.find_element(*BasePageLocators.CATEGORY_LINK)
            go.click()

    def choose_city_moscow(self):
        with allure.step('Выбран гео Москва'):
            save = self.browser.find_element(*BasePageLocators.CHOOSE_MOSCOW)
            save.click()
            button = self.browser.find_element(*BasePageLocators.SAVE_CITY)
            button.click()

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

    def is_logo_present(self):
        with allure.step('Проверка наличия логотипа'):
            element = self.browser.find_element(*BasePageLocators.LOGO)
            src = element.get_attribute('src')
            assert '/images/logo2020.svg' in src, "Логотип отсутствует"

    def __init__(self, browser, link, timeout=10):
        self.browser = browser
        self.link = link
        self.browser.implicitly_wait(timeout)

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    def is_not_stretch_present(self):
        with allure.step('Проверка наличия растяжки'):
            assert self.is_element_present(*BasePageLocators.STRETCH), "Растяжка отсутствует"

    def is_stretch_present(self):
        with allure.step('Проверка отсутствия растяжки'):
            assert self.is_not_element_present(*BasePageLocators.STRETCH), "Растяжка присутствует"

    def is_stretch_timer_present(self):
        with allure.step('Проверка наличия таймера у растяжки'):
            assert self.is_not_element_present(*BasePageLocators.STRETCH_TIMER), "Таймер растяжки присутствует"

    def open(self):
        self.browser.get(self.link)
