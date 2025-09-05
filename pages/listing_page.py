from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .locators import ListingPageLocators
from .base_page import BasePage
import allure
import time
from selenium.webdriver.common.action_chains import ActionChains


class ListingPage(BasePage):
    def add_to_compare(self):
        with allure.step('Добавили товар в сравнения'):
            actions = ActionChains(self.browser)
            fav = self.browser.find_element(*ListingPageLocators.ADD_TO_COMPARE_LISTING)
            actions.move_to_element(fav).perform()
            time.sleep(1)
            fav.click()

    def add_to_favorite(self):
        with allure.step('Добавили товар в избранное'):
            actions = ActionChains(self.browser)
            fav = self.browser.find_element(*ListingPageLocators.ADD_TO_FAVORITE_LISTING)
            actions.move_to_element(fav).perform()
            time.sleep(1)
            fav.click()

    def go_to_compare(self):
        with allure.step('Переход в сравнения'):
            go = self.browser.find_element(*ListingPageLocators.COMPARE_ICON_LISTING)
            go.click()

    def go_to_favorite(self):
        with allure.step('Переход в избранное'):
            go = self.browser.find_element(*ListingPageLocators.FAV_ICON_LISTING)
            go.click()

    def go_to_item1(self):
        with allure.step('Переход в КТ'):
            go = self.browser.find_element(*ListingPageLocators.ITEM_LNK)
            go.click()

    def is_any_good_in_compare(self):
        with allure.step('В сравнениях есть товары'):
            assert self.is_element_present(*ListingPageLocators.COMPARE_COUNT_LISTING)

    def is_any_good_in_favorite(self):
        with allure.step('В избранном есть товары'):
            assert self.is_element_present(*ListingPageLocators.FAVORITE_COUNT_LISTING)

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

    def open(self):
        self.browser.get(self.link)

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

    # noinspection PyTypeChecker
    def is_disappeared(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException). \
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True
