import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions

from acceptance_core_py.core import driver
from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.helpers import env


def wait_for_load() -> bool:
    try_count = 0
    max_try_count = env.get_waiting_default_timeout()
    get_page_state_js = "return document.readyState"
    state = str(driver_actions.execute_js(get_page_state_js))

    while state != "complete":
        if try_count > max_try_count:
            logging.error(f"Could not waiting for page load for {max_try_count} seconds")
            return False

        try_count += 1
        state = str(driver_actions.execute_js(get_page_state_js))
        logging.info(f"Current page state = {state}, try = {try_count} of {max_try_count}")
        time.sleep(1)

    logging.info(f"Successfully loading page with state '{state}' for {try_count} seconds")
    return True


def wait_for_element_exists(selector: str, message: str = None, timeout: int = None):
    timeout = get_waiting_timeout_from_env_if_necessary(timeout)
    if message is None:
        message = f"Element with selector '{selector}' did not exists for {timeout} seconds"

    logging.info(f"Waiting for existing element with selector '{selector}' for {timeout} seconds")
    return ui.WebDriverWait(driver.instance, timeout).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector)), message)


def wait_for_element_clickable(selector: str, message: str = None, timeout: int = None):
    timeout = get_waiting_timeout_from_env_if_necessary(timeout)
    if message is None:
        message = f"Element with selector '{selector}' did not become clickable for {timeout} seconds"

    logging.info(f"Waiting element with selector '{selector}' being clickable for {timeout} seconds")
    return ui.WebDriverWait(driver.instance, timeout).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, selector)), message)


def wait_for_element_visible(selector: str, message: str = None, timeout: int = None):
    timeout = get_waiting_timeout_from_env_if_necessary(timeout)
    if message is None:
        message = f"Element with selector '{selector}' did not become visible for {timeout} seconds"

    logging.info(f"Waiting for visibility element with selector '{selector}' for {timeout} seconds")
    return ui.WebDriverWait(driver.instance, timeout).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, selector)), message)


def get_waiting_timeout_from_env_if_necessary(timeout: int = None):
    if timeout is None:
        timeout = env.get_waiting_default_timeout()
        logging.debug(f"Set timeout from ENV-config in {timeout} seconds")
        return timeout

    logging.debug(f"Set timeout NOT from ENV-config in {timeout} seconds, probably from method's argument")
    return timeout
