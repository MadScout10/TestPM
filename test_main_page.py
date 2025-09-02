import pytest
from .pages.product_page import ProductPage
from .pages.main_page import MainPage
import time
import allure


class TestsForReview:
    @pytest.mark.need_review
    @allure.feature('Проверка добавления в корзину')
    @allure.story('Главная-Листинг-КТ-В корзину')
    @allure.title('Пользователь может добавить товар в корзину')
    def test_guest_can_add_product_to_basket(self, browser, initstage):
        link = initstage
        page = MainPage(browser, link)  # инициализируем Page Object
        page.open()
        page.basket_is_empty_mark_check() # проверяем что коорзина пуста
        page.go_to_category1()  # открываем каталог
        page.go_to_item1()  # открываем КТ
        product_page = ProductPage(browser, browser.current_url)  # инициализируем Page Object для КТ
        product_page.add_to_cart()  # добавляем товар в корзину
        product_page.basket_is_not_empty_mark_check() # проверяем, что товар добавлен в корзину
        product_page.check_product_name() # проверяем имя товара
        time.sleep(5)  # доп.ожидание, чтобы убедиться что все ок


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
        page.is_stretch_present()  # проверить наличие растяжки

    @pytest.mark.smoke
    @allure.title('Пример упавшего теста')
    def test_failure(self, browser, initstage):
        link = initstage
        page = MainPage(browser, link)  # инициализируем Page Object
        page.open()
        page.go_to_basket_page()  # пробуем зайти в пустую корзину
