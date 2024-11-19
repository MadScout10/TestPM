import pytest
from .pages.listing_page import ListingPage
# from .pages.main_page import MainPage
import time
import allure


class TestsSmoke:
    @pytest.mark.smoke
    @allure.title('Проверка открытия каталожной страницы')
    def test_open_listing_gost(self, browser, initstage):
        link = initstage + 'catalog/gostinaya/'
        page = ListingPage(browser, link)  # инициализируем Page Object
        page.open()
        page.is_listing_opened_gost()  # проверить какая страница открыта

    @pytest.mark.smoke
    @allure.title('Проверка открытия категорийной страницы')
    def test_open_listing_div(self, browser, initstage):
        link = initstage + "category/mebel-dlya-doma/divany/"
        page = ListingPage(browser, link)  # инициализируем Page Object
        page.open()
        page.is_listing_opened_div()  # проверить какая страница открыта
        time.sleep(10)
