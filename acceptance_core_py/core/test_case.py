from acceptance_core_py.core import driver
from acceptance_core_py.core.actions import driver_actions


class TestCase:
    def setup(self):
        driver.initialize()
        # Example of add cookie in beginning of each test
        driver_actions.add_cookie_to_domain("hide_popups", "true")

    def teardown(self):
        driver.close_driver()
