import pytest
from pages.listing_page import ListingPage
# from .pages.basket_page import BasketPage
from .pages.v2_page import V2Page
# from .pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class TestsForReview:
    @pytest.mark.need_review
    @allure.title("Проверка добавления в избранное")
    def test_add_to_favorite_review(self, browser, initstage):
        link = initstage + "category/mebel-dlya-doma/igrovye-kresla/"
        listing = ListingPage(browser, link)
        listing.open()
        listing.add_to_favorite()
        listing.is_any_good_in_favorite()
        name = browser.find_element(By.CLASS_NAME, 'good__title').text
        listing.go_to_favorite()
        v2name = browser.find_element(By.CSS_SELECTOR, 'a.favorite-good-card__name').text
        print(f'listing = {name} favorite = {v2name}')
        assert name.lower() == v2name.lower()

    @pytest.mark.need_review
    @allure.title("Проверка добавления в сравнения")
    def test_add_to_compare_review(self, browser, initstage):
        link = initstage + "category/mebel-dlya-doma/igrovye-kresla/"
        listing = ListingPage(browser, link)
        listing.open()
        listing.add_to_compare()
        listing.is_any_good_in_compare()
        name = browser.find_element(By.CLASS_NAME, 'good__title').text
        listing.go_to_compare()
        v2name = browser.find_element(By.CSS_SELECTOR, 'a.favorite-good-card__name').text
        print(f'listing = {name} favorite = {v2name}')
        assert name.lower() == v2name.lower()


class TestsSmoke:
    @pytest.mark.smoke
    @allure.title("Проверка открытия избранного")
    def test_is_favourite_open(self, browser, initstage):
        link = initstage + "v2/my/compare/"
        page = V2Page(browser, link)
        page.open()
        page.is_v2_opened()

    @pytest.mark.smoke
    @allure.title("Проверка открытия сравнения")
    def test_is_compare_open(self, browser, initstage):
        link = initstage + "v2/my/compare/"
        page = V2Page(browser, link)
        page.open()
        page.is_v2_opened()

    @pytest.mark.smoke
    @allure.title("Проверка добавления в избранное")
    def test_add_to_favorite(self, browser, initstage):
        link = initstage + "category/mebel-dlya-doma/igrovye-kresla/"
        listing = ListingPage(browser, link)
        listing.open()
        listing.add_to_favorite()
        listing.is_any_good_in_favorite()

    @pytest.mark.smoke
    @allure.title("Проверка открытия избранного")
    def test_add_to_compare(self, browser, initstage):
        link = initstage + "category/mebel-dlya-doma/igrovye-kresla/"
        listing = ListingPage(browser, link)
        listing.open()
        listing.add_to_compare()
        listing.is_any_good_in_compare()



