from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import visibility_of_element_located, invisibility_of_element, \
    presence_of_all_elements_located, element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait
import pytest
from selenium.webdriver.edge.webdriver import WebDriver as e_wd
from selenium.webdriver.chrome.webdriver import WebDriver as c_wd
from selenium.webdriver.safari.webdriver import WebDriver as s_wd
from selenium.webdriver.firefox.webdriver import WebDriver as f_wd


class Titanium:
    """ Titanium gave handy action over selenium web


    """
    def _get_attribute(self):
        value = None
        for i in dir(pytest):
            value = getattr(pytest, i)
            if isinstance(value, (e_wd, c_wd, s_wd, f_wd)):
                return value

    def __init__(self, web_driver=self._get_attribute()):
        """ Initialize web_driver to the object

        parameters:
        web_driver (selenium.webdriver): webdriver object

        """
        # value = None
        # for i in dir(pytest):
        #     value = getattr(pytest, i)
        #     if isinstance(value, (e_wd, c_wd, s_wd, f_wd)):
        #         value = value

        self.driver = web_driver
        self.action_chains = ActionChains(self.driver)

    def click_element(self, locator: str, by_type=By.XPATH):
        """ click on web element

        parameters:
        by_type (str): type of element
        locator (str): locator

        return None"""
        self.get_element(locator, by_type).click()

    def get_element(self, locator: str, by_type=By.XPATH) -> WebElement:
        """ get web element

        parameters:
        by_type (str): type of element
        locator (str): locator

        return WebElement
        """
        return self.driver.find_element(by_type, locator)

    def get_elements(self, locator: str, by_type=By.XPATH) -> list:
        """ get web elements

        parameters:
        by_type (str): type of element
        locator (str): locator

        return list of WebElement
        """
        return self.driver.find_elements(by_type, locator)

    def send_keys(self, locator: str, by_type=By.XPATH, value=""):
        """ sends value to the web element

        parameters:
        by_type (str): type of element
        locator (str): locator
        value (str): value

        return None
        """
        self.get_element(locator, by_type).send_keys(value)

    def scroll_to_element(self, locator: str, by_type=By.XPATH):
        """ scroll to element

        parameters:
        by_type (str): type of element
        locator (str): locator

        return None
        """
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                                   self.get_element(locator, by_type))

    def js_click_element(self, locator: str, by_type=By.XPATH):
        """ js click on web element

        parameters:
        by_type (str): type of element
        locator (str): locator

        return None
        """
        self.driver.execute_script("arguments[0].click()", self.get_element(locator, by_type))

    def element_visible(self, locator: str, by_type=By.XPATH) -> bool:
        """ check if element is visible

        parameters:
        by_type (str): type of element
        locator (str): locator

        return bool
        """
        try:
            WebDriverWait(self.driver, timeout=10).until(visibility_of_element_located((by_type, locator)))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def element_invisible(self, locator: str, by_type=By.XPATH) -> bool:
        """ check if element is invisible

        parameters:
        by_type (str): type of element
        locator (str): locator

        return bool
        """
        try:
            WebDriverWait(self.driver, timeout=10).until(invisibility_of_element(
                self.get_element(locator, by_type)))
            return True
        except TimeoutException:
            return False

    def element_present(self, locator: str, by_type=By.XPATH) -> bool:
        """ check if element is present

        parameters:
        by_type (str): type of element
        locator (str): locator

        return bool
        """
        try:
            WebDriverWait(self.driver, timeout=10).until(presence_of_all_elements_located((by_type, locator)))
            return True
        except TimeoutException:
            return False

    def move_to_element(self, locator: str, by_type=By.XPATH):
        """ move to element

        parameters:
        by_type (str): type of element
        locator (str): locator

        return None
        """
        self.action_chains.move_to_element(self.get_element(locator, by_type)).perform()

    def move_to_offset(self, x_offset=5, y_offset=5):
        """ move to offset

        parameters:
        x_offset (int): x offset
        y_offset (int): y offset

        return None
        """
        self.action_chains.move_by_offset(x_offset, y_offset).perform()

    def get_text(self, locator: str, by_type=By.XPATH) -> str:
        """ get text from element

        parameters:
        by_type (str): type of element
        locator (str): locator

        return str
        """
        return self.get_element(locator, by_type).text

    def element_clickable(self, locator: str, by_type=By.XPATH) -> bool:
        """
        check if element is clickable

        parameters
        :param locator:
        :param by_type:
        :return: bool
        """
        try:
            WebDriverWait(self.driver, 10).until(element_to_be_clickable((by_type, locator)))
            return True
        except TimeoutException:
            return False

    def get_title(self) -> str:
        """
        get title

        :return: str
        """
        return self.driver.title

    def open_new_window(self, index=0):
        """
        open new window

        parameters:
        index (int):
        :return: None
        """
        self.driver.execute_script("window.open()")
        if not index == 0:
            self.driver.switch_to.window(self.driver.window_handles[index])

    def click_visible_element(self, locator: str, by_type=By.XPATH):
        """
        click visible element

        parameters
        :param locator: str
        :param by_type: str
        :return:
        """
        flag = self.element_visible(locator, by_type)
        if flag:
            self.js_click_element(locator, by_type)
        else:
            raise TimeoutException
