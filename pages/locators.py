from selenium.webdriver.common.by import By


class BasePageLocators:
    BASKET_LINK = (By.CSS_SELECTOR, "div.cart-block")
    BASKET_EMPTY = (By.CSS_SELECTOR, "div.cart-block-info")
    CATEGORY_LINK = (By.CLASS_NAME, "header-nav__category_1")
    CHOOSE_MOSCOW = (By.CSS_SELECTOR, "div.city-modal__examples > :nth-child(1)")
    SAVE_CITY = (By.ID, "city-save")
    STRETCH = (By.ID, 'promoStretching')
    STRETCH_TIMER = (By.CLASS_NAME, 'countdown active')
    LOGO = (By.CSS_SELECTOR, 'a.header-logo img')


class ListingPageLocators:
    LISTING_H1 = (By.CSS_SELECTOR, 'div h1')
    ITEM_LNK = (By.CLASS_NAME, "good__link-wrapper")


class ProductPageLocators:
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "add-to-cart-button")
    NAME_OF_PRODUCT = (By.CLASS_NAME, "catalog-header__title")
    NAME_OF_ADDED_PRODUCT = (By.CSS_SELECTOR, "h3.title")
    PRICE_OF_ADDED_PRODUCT = (By.CLASS_NAME, "item-price-total")
    PRICE_OF_PRODUCT = (By.CSS_SELECTOR, "span.price-item__price span.price_no_rub")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "modal-helper cart-modal")
    MODAL_CHECKOUT = (By.CLASS_NAME, "button_checkout")
    COLORS = (By.CSS_SELECTOR, "ul.pr-det_block-color")
    COLOR1 = (By.CSS_SELECTOR, "ul.pr-det_block-color > :nth-child(1)")
    PHOTOS = (By.CLASS_NAME, "prod-slider ")


class BasketPageLocators:
    BASKET_ITEMS = (By.CSS_SELECTOR, "div.basket__left")
    CHECKOUT = (By.CLASS_NAME, 'basket-order__next-step')
    PHONE = (By.NAME, 'order[phone]')
    BUY = (By.CLASS_NAME, 'basket-order__checkout')
    ORDER_NUMBER = (By.CSS_SELECTOR, 'div.cart-info :nth-child(3) h2')
