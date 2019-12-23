import logging
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import TouchActions
from selenium.webdriver.remote.webelement import WebElement

from acceptance_core_py.core import driver
from acceptance_core_py.core.actions import waiting_actions
from acceptance_core_py.core.exception.at_exception import ATException
from acceptance_core_py.helpers import env


# Click/tap methods

def click(selector: str):
    if env.is_enable_mobile_emulation_mode():
        logging.info(f"Native tap on element with selector '{selector}'")
        TouchActions(driver.instance).tap(locate_element(selector))
    else:
        logging.info(f"Native click on element with selector '{selector}'")
        locate_element(selector).click()


def click_by_html(selector: str):
    logging.info(f"Click on element with selector '{selector}' by HTML")
    execute_js(get_dom_object(selector, "click()"))
    waiting_actions.wait_for_load()


# Openers methods

def open_relative_url(relative_url: str):
    opened_url = env.get_base_url() + relative_url
    logging.info("Opening URL " + opened_url)
    driver.instance.get(opened_url)
    waiting_actions.wait_for_load()


# Grabber methods

def grab_text_from_element(selector: str) -> str:
    if is_element_not_exists(selector):
        logging.info(f"Can't grab text from selector '{selector}': element do not exist.")
        return ""

    element = locate_element(selector)
    grabbed_text = element.text() if element.is_displayed() else grab_text_from_hidden_element(selector)
    logging.info(f"Grabbed text '{grabbed_text}' from selector '{selector}'")
    return grabbed_text


def grab_text_from_hidden_element(selector: str) -> str:
    text = execute_js("return " + get_dom_object(selector, "textContent"))
    logging.debug(f"Grabbed text '{text}' from hidden selector '{selector}' by JS")
    return text


def grab_text_from_hidden_elements(selector: str) -> List:
    result = list()
    i = 0
    for element in locate_elements(selector):
        grabbed_text = element.text() if element.is_displayed() else execute_js(
            f"return $('{selector}').eq({i}).text();")
        result.append(grabbed_text)
        i += 1
    return result


# Checking anything methods

def is_element_exists(selector: str) -> bool:
    logging.info(f"Check if an element exists '{selector}'")
    return len(locate_elements(selector)) > 0


def is_element_not_exists(selector: str) -> bool:
    logging.info(f"Check if an element not exists '{selector}'")
    return len(locate_elements(selector)) == 0


# Locate element or elements methods

def locate_element(css_selector: str) -> WebElement:
    try:
        return driver.instance.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        raise ATException("At this time only CSS selectors allowed. Invalid selector: " + css_selector)


def locate_elements(css_selector: str) -> List[WebElement]:
    try:
        return driver.instance.find_elements_by_css_selector(css_selector)
    except NoSuchElementException:
        raise ATException("At this time only CSS selectors allowed. Invalid selector: " + css_selector)


# Executing JS methods

def get_dom_object(css_selector: str, property_or_method_to_execute: str = None) -> str:
    return f"document.querySelector('{css_selector}')" + \
           ('' if property_or_method_to_execute is None else f".{property_or_method_to_execute}")


def execute_js(js: str, *args):
    return driver.instance.execute_script(js, args)
