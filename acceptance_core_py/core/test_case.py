import logging
import unittest

from acceptance_core_py.core import driver
from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.helpers.utils import strings_utils


class TestCase(unittest.TestCase):
    def setUp(self):
        driver.initialize()
        # TODO (Delete) Example of adding cookie in beginning of each test
        driver_actions.add_cookie_to_domain("hide_popups", "true")

    def tearDown(self):
        driver.close_driver()

    # Asserts with advanced logging (add your assert below)

    def assert_selector_exists(self, css_selector: str, comment_message: str = "Selector does not exists"):
        logging.info(f"Asserting that selector '{css_selector}' is exists")
        assert driver_actions.is_element_exists(css_selector), \
            f"Assertion failed! Message: {comment_message}. Selector '{css_selector}' does not exists"

    def assert_selector_not_exists(self, css_selector: str, comment_message: str = "Selector exists and it is bad"):
        logging.info(f"Asserting that selector '{css_selector}' does not exists")
        assert driver_actions.is_element_not_exists(css_selector), \
            f"Assertion failed! Message: {comment_message}. Selector '{css_selector}' is exists and it is bad"

    def assert_selector_visible(self, css_selector: str, comment_message: str = "Selector does not visible"):
        logging.info(f"Asserting that selector '{css_selector}' is visible")
        assert driver_actions.is_element_visible(css_selector), \
            f"Assertion failed! Message: {comment_message}. Selector '{css_selector}' does not visible"

    def assert_selector_not_visible(self, css_selector: str,
                                    comment_message: str = "Selector is visible and it is bad"):
        logging.info(f"Asserting that selector '{css_selector}' does not visible")
        assert driver_actions.is_element_not_visible(css_selector), \
            f"Assertion failed! Message: {comment_message}. Selector '{css_selector}' is visible and it is bad"

    def assert_strings_pattern(self, needle: str, haystack: str,
                               comment_message: str = "Needle string does not in haystack string"):
        logging.info(f"Asserting that needle string '{needle}' is in haystack string '{haystack}'")
        assert strings_utils.is_string_found_in(needle, haystack), \
            f"Assertion failed! Message: {comment_message}. Needle string '{needle}' is not in haystack string '{haystack}'"

    def assert_equal(self, expected, actual, comment_message: str = "Expected and actual do not equals"):
        logging.info(f"Asserting that expected '{str(expected)}' is equals with actual '{str(actual)}'")
        self.assertEqual(first=expected, second=actual, msg=comment_message)

    def assert_almost_equal(self, expected, actual, delta=None, places=None,
                            comment_message: str = "Expected and actual does not almost equals"):
        logging.info(f"Asserting that expected '{str(expected)}' is equals with actual '{str(actual)}' "
                     f"with delta '{str(delta)}'")
        self.assertAlmostEqual(first=expected, second=actual, places=places, delta=delta, msg=comment_message)

    def assert_not_equal(self, expected, actual, comment_message: str = "Expected and actual are equals and it is bad"):
        logging.info(f"Asserting that expected '{str(expected)}' is not equals with actual '{str(actual)}'")
        self.assertNotEqual(first=expected, second=actual, msg=comment_message)
