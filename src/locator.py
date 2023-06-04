from selenium.webdriver.common.by import By

class LocatorAvito:
    NEXT_BTN = (By.CSS_SELECTOR, "[data-marker*='pagination-button/next']")
    ADS = (By.CSS_SELECTOR, "[data-marker='item']")
    AD_ID = (By.CSS_SELECTOR, "[data-marker='item-view/item-id']")
    NAME = (By.CSS_SELECTOR, "[data-marker='item-view/title-info']")
    PRICE = (By.CSS_SELECTOR, "[class*='style-item-view-price']")
    ADDRESS = (By.CSS_SELECTOR, "[itemprop='address']")
    DESCRIPTIONS = (By.CSS_SELECTOR, "[class*='item-description']")
    DATE_PUBLIC = (By.CSS_SELECTOR, "[data-marker='item-view/item-date']")
    TOTAL_VIEWS = (By.CSS_SELECTOR, "[data-marker='item-view/total-views']")
    URL = (By.CSS_SELECTOR, "[data-marker='item-title']")
    CLOSED = (By.CSS_SELECTOR, "[data-marker='item-view/closed-warning']")