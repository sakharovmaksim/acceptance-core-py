from acceptance_core_py.core.web_driver import WD


class TestClass:
    driver = object

    def setup(self):
        print("Creating WebDriver...")
        self.driver = WD().create_web_driver()

    def teardown(self):
        print("Quit WebDriver. Bye-bye")
        self.driver.quit()

    def test_simple_test(self):
        self.driver.open_relative_url("")
