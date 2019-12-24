import logging
import tldextract
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import TouchActions
from selenium.webdriver.remote.webelement import WebElement

from acceptance_core_py.core import driver
from acceptance_core_py.core.actions import waiting_actions
from acceptance_core_py.core.exception.at_exception import ATException
from acceptance_core_py.helpers import env
from acceptance_core_py.helpers.utils import strings_utils


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

def open_relative_url(relative_url: str = ""):
    opened_url = env.get_base_url() + relative_url
    logging.info("Opening URL " + opened_url)
    driver.instance.get(opened_url)
    waiting_actions.wait_for_load()


def open_direct_url(url: str):
    logging.info(f"Opening direct URL '{url}'")
    driver.instance.get(url)


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


# Managing cookies methods

def add_cookie_to_domain(name: str, value: str, domain: str = None):
    if domain is None:
        domain = get_domain()

    open_relative_url()

    logging.info(f"Add cookie with name: '{name}', value: '{value}', domain: '{domain}'")
    driver.instance.add_cookie({'name': name, 'value': value, 'domain': domain})

    if not get_cookie_with_name(name):
        raise ATException(f"Could not set cookie with name '{name}' for domain '{domain}'")


def get_all_cookies() -> dict:
    logging.info(f"Get all cookies")
    return driver.instance.get_cookies()


def get_cookie_with_name(cookie_name: str) -> dict:
    logging.info(f"Get cookie with name {cookie_name}")
    return driver.instance.get_cookie(cookie_name)


def clear_all_cookies():
    logging.info("Clearing all cookies")
    driver.instance.delete_all_cookies()


def clear_local_storage():
    logging.info("Clearing local storage")
    execute_js("localStorage.clear();")


def clear_session_storage():
    logging.info("Clearing session storage")
    execute_js("sessionStorage.clear();")


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


# Browser direct methods

def reload_page():
    logging.info("Reloading page")
    driver.instance.refresh()
    waiting_actions.wait_for_load()


def go_back():
    logging.info("Go back in browser")
    driver.instance.back()
    waiting_actions.wait_for_load()


def get_url() -> str:
    url = driver.instance.current_url
    logging.info(f"Got URL from browser '{url}'")
    return url


def get_domain() -> str:
    """Returns extended domain string"""
    url = get_url()
    if len(url) == 0 or strings_utils.is_string_found_in("data:", url):
        logging.info(f"Got bad URL '{url}' from browser, getting URL from ENV")
        url = env.get_base_url()

    extract_result = tldextract.extract(url)

    sub_domain = extract_result.subdomain
    domain = extract_result.domain
    suffix = extract_result.suffix
    extended_domain = sub_domain + "." + domain + "." + suffix

    logging.info(f"Got domain '{extended_domain}' from URL '{url}'")
    return extended_domain


# Executing JS methods

def get_dom_object(css_selector: str, property_or_method_to_execute: str = None) -> str:
    return f"document.querySelector('{css_selector}')" + \
           ('' if property_or_method_to_execute is None else f".{property_or_method_to_execute}")


def execute_js(js: str, *args):
    return driver.instance.execute_script(js, args)
