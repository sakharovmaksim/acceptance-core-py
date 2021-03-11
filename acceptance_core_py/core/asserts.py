import logging
import unittest

from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.selector import Selector
from acceptance_core_py.helpers.allure.steps import assert_code_step
from acceptance_core_py.helpers.utils import strings_utils


def assert_selector_exists(
    css_selector: Selector, comment_message: str = "Selector does not exists"
):
    logging.info(f"Asserting that '{css_selector=}' is exists")
    assert_code_step(f"{comment_message}. '{css_selector=}'")
    assert driver_actions.is_element_exists(
        css_selector
    ), f"Assertion failed! Message: '{comment_message}'. '{css_selector=}' does not exists"


def assert_selector_not_exists(
    css_selector: Selector, comment_message: str = "Selector exists and it is bad"
):
    logging.info(f"Asserting that '{css_selector=}' does not exists")
    assert_code_step(f"{comment_message}. '{css_selector=}'")
    assert driver_actions.is_element_not_exists(
        css_selector
    ), f"Assertion failed! Message: '{comment_message}'. '{css_selector=}' is exists and it is bad"


def assert_selector_visible(
    css_selector: Selector, comment_message: str = "Selector does not visible"
):
    logging.info(f"Asserting that '{css_selector=}' is visible")
    assert_code_step(f"{comment_message}. '{css_selector=}'")
    assert driver_actions.is_element_visible(
        css_selector
    ), f"Assertion failed! Message: '{comment_message}'. '{css_selector=}' does not visible"


def assert_selector_not_visible(
    css_selector: Selector, comment_message: str = "Selector is visible and it is bad"
):
    logging.info(f"Asserting that '{css_selector=}' does not visible")
    assert_code_step(f"{comment_message}. '{css_selector=}'")
    assert driver_actions.is_element_not_visible(
        css_selector
    ), f"Assertion failed! Message: '{comment_message}'. '{css_selector=}' is visible and it is bad"


def assert_strings_pattern(
    needle: str,
    haystack: str,
    comment_message: str = "Needle string does not in haystack string",
):
    logging.info(f"Asserting that '{needle=}' is in '{haystack=}'")
    assert_code_step(f"{comment_message}. '{needle=}', '{haystack=}'")
    assert strings_utils.is_string_found_in(needle, haystack), (
        f"Assertion failed! Message: '{comment_message}'. "
        f"'{needle=}' is not in '{haystack=}'"
    )


def assert_equal(
    expected, actual, comment_message: str = "Expected and actual is not equals"
):
    logging.info(f"Asserting that '{expected=}' is equals with actual '{actual=}'")
    assert_code_step(f"{comment_message}. '{expected=}', '{actual=}'")
    unittest.TestCase().assertEqual(first=expected, second=actual, msg=comment_message)


def assert_collection_len(
    expected_len,
    actual_collection,
    comment_message: str = "Actual collection len is not equal expected value",
):
    actual_collection = len(actual_collection)
    logging.info(
        f"Asserting that expected collection len '{expected_len}' "
        f"is equals with actual collection len. Collection '{str(actual_collection)}'"
    )
    assert_code_step(
        f"{comment_message}. '{expected_len=}', '{str(actual_collection)=}'"
    )
    unittest.TestCase().assertEqual(
        first=expected_len, second=actual_collection, msg=comment_message
    )


def assert_almost_equal(
    expected,
    actual,
    delta=None,
    places=None,
    comment_message: str = "Expected and actual does not almost equals",
):
    logging.info(
        f"Asserting that '{expected=}' is equals with '{actual=}' with '{delta=}'"
    )
    assert_code_step(f"{comment_message}. '{expected=}', '{actual=}'")
    unittest.TestCase().assertAlmostEqual(
        first=expected, second=actual, places=places, delta=delta, msg=comment_message
    )


def assert_not_equal(
    expected,
    actual,
    comment_message: str = "Expected and actual are equals and it is bad",
):
    logging.info(f"Asserting that '{expected=}' is not equals with '{actual=}'")
    assert_code_step(f"{comment_message}. {actual=}, {expected=}")
    unittest.TestCase().assertNotEqual(
        first=expected, second=actual, msg=comment_message
    )


def assert_greater(
    first, second, comment_message: str = "First value is not greater than second"
):
    logging.info(f"Asserting that '{first=}' greater than '{second=}'")
    assert_code_step(f"{comment_message}. {first=}, {second=}")
    unittest.TestCase().assertGreater(a=first, b=second, msg=comment_message)


def assert_greater_equal(
    first,
    second,
    comment_message: str = "First value is not greater with equal than second",
):
    logging.info(f"Asserting that '{first=}' greater with equal than '{second=}'")
    assert_code_step(f"{comment_message}. {first=}, {second=}")
    unittest.TestCase().assertGreaterEqual(a=first, b=second, msg=comment_message)


def assert_less_equal(
    first,
    second,
    comment_message: str = "First value is not less with equal than second",
):
    logging.info(f"Asserting that '{first=}' less with equal than '{second=}'")
    assert_code_step(f"{comment_message}. {first=}, {second=}")
    unittest.TestCase().assertLessEqual(a=first, b=second, msg=comment_message)


# Use for testing regex: https://regex101.com/#pcre


def assert_regex(
    text, expected_regex, comment_message="Expected regex is not find in text"
):
    logging.info(f"Asserting that '{expected_regex=}' found in '{text=}'")
    assert_code_step(f"{comment_message}. '{text=}', '{expected_regex=}'")
    unittest.TestCase().assertRegex(text, expected_regex, comment_message)


def assert_not_regex(
    text, unexpected_regex, comment_message="Expected regex is find in text. It's bad"
):
    logging.info(f"Asserting that '{unexpected_regex=}' found in '{text=}'")
    assert_code_step(f"{comment_message}. '{text=}', '{unexpected_regex=}'")
    unittest.TestCase().assertNotRegex(text, unexpected_regex, comment_message)
