import pytest
# from .pages.basket_page import BasketPage
from .pages.product_page import ProductPage
from .pages.base_page import BasePage
# import time
import allure


class TestsSmoke:
    @pytest.mark.smoke
    @allure.title("Проверка открытия КТ")
    def test_is_prodcard_open(self, browser, initstage):
        link = initstage + "category/mebel-dlya-doma/divany/pryamye-divany/goods-divan_oazis-id157113/"
        page = ProductPage(browser, link)
        page.open()
        page.is_prodcard_open()

    @pytest.mark.regression
    @allure.title("Проверка наличия кнопки купить в КТ")
    def test_is_buybutton_present(self, browser, initstage):
        link = initstage + "category/mebel-dlya-doma/divany/pryamye-divany/goods-divan_oazis-id157113/"
        page = ProductPage(browser, link)
        page.open()
        page.is_buybutton_not_present()

    @pytest.mark.smoke
    @allure.title("Проверка работы кнопки купить в КТ")
    def test_is_buybutton_works(self, browser, initstage):
        link = initstage + "category/mebel-dlya-doma/divany/pryamye-divany/goods-divan_oazis-id157113/"
        page = ProductPage(browser, link)
        page.open()
        page.is_buybutton_work()
        page.check_product_name()
        page.check_price()

    @pytest.mark.smoke
    @allure.title("Проверка перехода в корзину из КТ")
    def test_go_to_cart_after_bb(self, browser, initstage):
        link = initstage + "category/mebel-dlya-doma/divany/pryamye-divany/goods-divan_oazis-id157113/"
        page = ProductPage(browser, link)
        page.open()
        page.add_to_cart()
        page.go_to_cart_after_buybutton()
        cart = BasePage(browser, browser.current_url)
        cart.basket_is_not_empty_mark_check()
