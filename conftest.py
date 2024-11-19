import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as OptionsFirefox
from .pages.main_page import MainPage


# Запуск теста производить примерно так: pytest -s -v --alluredir results "имя теста"


# параметры запуска тестов
def pytest_addoption(parser):
    parser.addoption('--browser_name',
                     action='store',
                     default="chrome",
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language',
                     action='store',
                     default='ru',
                     help='Choose language')
    parser.addoption("--stage",
                     action='store',
                     default='https://pm.ru/',
                     help='Base URL for the API tests')


# Запуск браузера(для каждой функции)
@pytest.fixture(scope="function")  # по умолчанию запускается для каждой функции
def browser(request):
    browser_name = request.config.getoption("browser_name")  # --browser_name='браузер'
    user_language = request.config.getoption("language")  # --language='язык'
    if browser_name == "chrome":
        options = Options()
        options.add_experimental_option('prefs',
                                        {'intl.accept_languages': user_language})
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        print("\nstart Firefox browser for test..")
        options_firefox = OptionsFirefox()
        options_firefox.set_preference("intl.accept_languages", user_language)
        browser = webdriver.Firefox(options=options_firefox)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser
    browser.quit()


@pytest.fixture(scope="function")  # по умолчанию запускается для каждой функции
def stage(request):
    return request.config.getoption('--stage')
    # возвращает значение, полученное из флага --stage


@pytest.fixture(scope='function')  # по умолчанию запускается для каждой функции
def initstage(browser, stage):
    init = MainPage(browser, stage)  # инициализация объекта(на случай если надо пб)
    init.open()
    url = browser.current_url  # берем текущий урл, чтобы передать его в тело теста
    return url
