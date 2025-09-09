import pytest
from selenium.webdriver.common.by import By
from .pages.basket_page import BasketPage
from .pages.listing_page import ListingPage
from .pages.product_page import ProductPage
from .pages.main_page import MainPage
import allure


class TestsForReview:
    @pytest.mark.need_review
    @allure.feature('Проверка добавления в корзину')
    @allure.story('Главная-Листинг-КТ-Корзина')
    @allure.title('Пользователь может добавить товар в корзину')
    def test_guest_can_add_product_to_basket(self, browser, initstage):
        link = initstage
        page = MainPage(browser, link)  # инициализируем Page Object
        page.open()
        page.basket_is_empty() # проверяем, что корзина пуста
        page.go_to_category1()  # открываем каталог
        listing = ListingPage(browser, browser.current_url)
        listing.go_to_item1()  # открываем КТ
        product_page = ProductPage(browser, browser.current_url)  # инициализируем Page Object для КТ
        product_page.add_to_cart()  # добавляем товар в корзину
        product_page.basket_is_not_empty()  # проверяем, что корзина не пуста
        product_page.check_product_name() # проверяем имя товара
        name = browser.find_element(By.CLASS_NAME, "catalog-header__title").text
        price = browser.find_element(By.CSS_SELECTOR, "span.price-item__price span.price_no_rub").text
        product_page.go_to_cart_after_buybutton() #  переходим в корзину
        cart = BasketPage(browser, browser.current_url)
        cart.items_in_basket_check() # проверяем наличие товаров в корзине
        cart.collect_item_info(name, price) # сравниваем имя, вариант и цену с данными в корзине

    # @pytest.mark.need_review
    @allure.title('Пользователь может добавить товар в корзину')
    def test_guest_can_add_product_to_basket_fail(self, browser, initstage):
        link = initstage + "category/mebel-dlya-doma/divany/pryamye-divany/goods-divan_oazis-id157113/"
        product_page = ProductPage(browser, link)
        product_page.open()
        false_price = "False price"
        product_page.add_to_cart()  # добавляем товар в корзину
        product_page.go_to_cart_after_buybutton()  # переходим в корзину
        price = "51 990"
        assert false_price == price, "НЕВЕРНАЯ ЦЕНА"


class TestsSmoke:
    @pytest.mark.smoke
    @allure.title('Проверка наличия логотипа на сайте')
    def test_logo_is_present(self, browser, initstage):
        link = initstage
        page = MainPage(browser, link)  # инициализируем Page Object
        page.open()
        page.is_logo_present()  # проверить наличие логотипа

    @pytest.mark.smoke
    @pytest.mark.xfail
    @allure.title('Проверка наличия растяжки')
    def test_is_stretch_present(self, browser, initstage):
        link = initstage
        page = MainPage(browser, link)  # инициализируем Page Object
        page.open()
        page.is_not_stretch_present()  # проверить наличие растяжки
