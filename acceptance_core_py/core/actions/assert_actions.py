import logging

from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.helpers.utils import strings_utils


def assert_selector_exists(css_selector: str, comment_message: str = "Selector does not exists"):
    logging.info(f"Asserting that selector '{css_selector}' is exists")
    assert driver_actions.is_element_exists(css_selector), \
        f"Assertion failed! Message: {comment_message}. Selector '{css_selector}' does not exists"


def assert_selector_not_exists(css_selector: str, comment_message: str = "Selector exists and it is bad"):
    logging.info(f"Asserting that selector '{css_selector}' does not exists")
    assert driver_actions.is_element_not_exists(css_selector), \
        f"Assertion failed! Message: {comment_message}. Selector '{css_selector}' is exists and it is bad"


def assert_selector_visible(css_selector: str, comment_message: str = "Selector does not visible"):
    logging.info(f"Asserting that selector '{css_selector}' is visible")
    assert driver_actions.is_element_visible(css_selector), \
        f"Assertion failed! Message: {comment_message}. Selector '{css_selector}' does not visible"


def assert_selector_not_visible(css_selector: str, comment_message: str = "Selector is visible and it is bad"):
    logging.info(f"Asserting that selector '{css_selector}' does not visible")
    assert driver_actions.is_element_not_visible(css_selector), \
        f"Assertion failed! Message: {comment_message}. Selector '{css_selector}' is visible and it is bad"


def assert_pattern(needle: str, haystack: str, comment_message: str = "Needle string does not in haystack string"):
    logging.info(f"Asserting that needle string '{needle}' is in haystack string '{haystack}'")
    assert strings_utils.is_string_found_in(needle, haystack), \
        f"Assertion failed! Message: {comment_message}. Needle string '{needle}' is not in haystack string '{haystack}'"
