from selenium.webdriver.common.by import By
import allure
import pytest


@pytest.mark.new
@pytest.mark.smoke
@allure.title('Проверка работы конфига')
def test_guest_should_see_login_link(browser):
    link = "http://selenium1py.pythonanywhere.com/"
    browser.get(link)
    browser.find_element(By.CSS_SELECTOR, "#login_link")
    print('Файл conftest.py работает исправно')
