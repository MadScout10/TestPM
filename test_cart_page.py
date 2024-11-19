import pytest
from .pages.basket_page import BasketPage
from .pages.product_page import ProductPage
# from .pages.base_page import BasePage
# import time
import allure


class TestsSmoke:
    @pytest.mark.smoke
    @allure.title('Проверка оформления заказа')
    def test_buy_something(self, browser):
        link = "https://pm.ru/category/mebel-dlya-doma/divany/pryamye-divany/goods-divan_oazis-id157113/"
        page = ProductPage(browser, link)
        page.open()
        page.add_to_cart()
        page.go_to_cart_after_buybutton()
        bpage = BasketPage(browser, link)
        bpage.checkout()
