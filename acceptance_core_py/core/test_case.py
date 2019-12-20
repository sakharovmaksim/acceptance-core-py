from acceptance_core_py.core import driver


class TestCase:
    def setup(self):
        driver.initialize()

    def teardown(self):
        driver.close_driver()
