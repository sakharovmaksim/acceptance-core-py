import inspect
import os
import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


class TestClass:
    def test_simple_test(self):
        frame = inspect.currentframe()

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['enableVNC'] = True
        capabilities['name'] = whoami(frame)

        driver = webdriver.Remote(
            "http://selenoid:selenoid-password@at2.butik.ru:4444/wd/hub",
            capabilities
        )

        driver.get(os.environ["HOST_URL"])
        time.sleep(5)
        driver.quit()


def whoami(frame):
    return inspect.getframeinfo(frame).function
