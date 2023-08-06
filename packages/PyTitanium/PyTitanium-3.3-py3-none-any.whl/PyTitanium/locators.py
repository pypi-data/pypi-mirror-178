from selenium.webdriver.common.by import By

XPATH = By.XPATH
ID = By.ID
CLASS_NAME = By.CLASS_NAME
CSS_SELECTOR = By.CSS_SELECTOR
PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
NAME = By.NAME
LINK_TEXT = By.LINK_TEXT
TAG_NAME = By.TAG_NAME

def locator_name(locator):
    locator = '[name="%s"]' % locator
    return locator, CSS_SELECTOR

def locator_id(locator):
    locator = '[id="%s"]' % locator
    return locator, CSS_SELECTOR

def locator_class_name(locator):
    locator = ".%s" % locator
    return locator, CSS_SELECTOR

def locator_xpath(locator):
    return locator, XPATH

def locator_link_text(locator):
    return locator, LINK_TEXT

def locator_partial_link_text(locator):
    return locator, PARTIAL_LINK_TEXT

def locator_tag_name(locator):
    return locator, TAG_NAME

def locator_css_selector(locator):
    return locator, CSS_SELECTOR

