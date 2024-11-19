from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from .locators import ListingPageLocators
from .base_page import BasePage
import allure


class ListingPage(BasePage):
    def go_to_item1(self):
        with allure.step('Переход в КТ'):
            go = self.browser.find_element(*ListingPageLocators.ITEM_LNK)
            go.click()

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def is_listing_opened_div(self):
        with allure.step('Проверка открытия'):
            li = self.browser.find_element(*ListingPageLocators.LISTING_H1)
            text = li.text
            assert text == "ДИВАНЫ", 'Неверный раздел листинга'

    def is_listing_opened_gost(self):
        with allure.step('Проверка открытия'):
            li = self.browser.find_element(*ListingPageLocators.LISTING_H1)
            text = li.text
            assert text == "МЕБЕЛЬ ДЛЯ ГОСТИНОЙ", 'Неверный раздел листинга'

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(ec.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

        return False

    def open(self):
        self.browser.get(self.link)
