from selenium.webdriver.common.by import By


class BasePageLocators:
    BASKET_LINK = (By.CSS_SELECTOR, "div.header__cart")
    BASKET_COUNT = (By.CSS_SELECTOR, 'span.header__cart-count')
    CATEGORY_LINK = (By.CLASS_NAME, "header-nav__category_1")
    CHOOSE_MOSCOW = (By.CSS_SELECTOR, "div.city-modal__examples > :nth-child(1)")
    SAVE_CITY = (By.ID, "city-save")
    STRETCH = (By.ID, 'promoStretching')
    STRETCH_TIMER = (By.CLASS_NAME, 'countdown active')
    LOGO = (By.CSS_SELECTOR, 'a.header-logo')
    LK_ICON = (By.CSS_SELECTOR, '')
    FAV_ICON = (By.CSS_SELECTOR, '')
    COMPARE_ICON = (By.CSS_SELECTOR, '')
    FAVORITE_COUNT_MAIN = (By.ID,'top-favorite-qty')
    COMPARE_COUNT_MAIN = (By.ID, 'top-compare-qty')


class ListingPageLocators:
    LISTING_H1 = (By.CSS_SELECTOR, 'div h1')
    ITEM_LNK = (By.CLASS_NAME, "good__link-wrapper")
    ADD_TO_FAVORITE_LISTING = (By.CLASS_NAME, 'good__favorite')
    ADD_TO_COMPARE_LISTING = (By.CLASS_NAME, 'good__compare')
    FAVORITE_COUNT_LISTING = (By.ID,'top-favorite-qty')
    COMPARE_COUNT_LISTING = (By.ID, 'top-compare-qty')
    LK_ICON_LISTING = (By.CSS_SELECTOR, '')
    FAV_ICON_LISTING = (By.CSS_SELECTOR, 'div.header-favorite')
    COMPARE_ICON_LISTING = (By.CSS_SELECTOR, 'div.header-compare')


class ProductPageLocators:
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "add-to-cart-button")
    NAME_OF_PRODUCT = (By.CLASS_NAME, "catalog-header__title")
    NAME_OF_ADDED_PRODUCT = (By.CSS_SELECTOR, "h3.title")
    PRICE_OF_ADDED_PRODUCT = (By.CLASS_NAME, "item-price-total")
    PRICE_OF_PRODUCT = (By.CSS_SELECTOR, "span.price-item__price span.price_no_rub")
    VARIANT_OF_PRODUCT = (By.CLASS_NAME, 'attribute-selected-value')
    SUCCESS_MESSAGE = (By.CLASS_NAME, "modal-helper cart-modal")
    MODAL_CHECKOUT = (By.CLASS_NAME, "button_checkout")
    COLORS = (By.CSS_SELECTOR, "ul.pr-det_block-color")
    COLOR1 = (By.CSS_SELECTOR, "ul.pr-det_block-color > :nth-child(1)")
    PHOTOS = (By.CLASS_NAME, "prod-slider ")
    FAVORITE_COUNT_PC = (By.ID,'top-favorite-qty')
    COMPARE_COUNT_PC = (By.ID, 'top-compare-qty')


class BasketPageLocators:
    BASKET_ITEMS = (By.CSS_SELECTOR, "div.basket__left")
    CHECKOUT = (By.CLASS_NAME, 'basket-order__next-step')
    PHONE = (By.NAME, 'order[phone]')
    BUY = (By.CLASS_NAME, 'basket-order__checkout')
    ORDER_NUMBER = (By.CSS_SELECTOR, 'div.cart-info :nth-child(3) h2')
    PRODNAME = (By.CSS_SELECTOR, 'a.detail-order-good-card__name')
    PRODVAR = (By.CSS_SELECTOR, 'li.detail-order-good-card__colors-item span')
    PRODPRICE = (By.CSS_SELECTOR, 'div.detail-order-good-card__prices > div.detail-order-good-card__current-price')


class V2PageLocators:
    V2LK_ICON = (By.CSS_SELECTOR, '')
    V2FAV_ICON = (By.CSS_SELECTOR, '')
    V2COMPARE_ICON = (By.CSS_SELECTOR, '')
    MENU_LK = (By.CSS_SELECTOR, '')
    MENU_FAV = (By.CSS_SELECTOR, '')
    MENU_ORDERS = (By.CSS_SELECTOR, '')
    MENU_COMPARE = (By.CSS_SELECTOR, '')
    MENU_EXIT = (By.CSS_SELECTOR, '')
    MENU_REVIEWS = (By.CSS_SELECTOR, '')
    MENU_SUPPORT = (By.CSS_SELECTOR, '')
    MENU = (By.CSS_SELECTOR, 'ul.column-navigation__list')
