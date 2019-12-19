from __future__ import annotations

import inspect
import os

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from acceptance_core_py.helpers import env


class WD:
    web_driver = None

    # Singleton pattern
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(WD, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance

    def __init__(self):
        if (self.__initialized): return
        self.__initialized = True
        self.create_web_driver()
        print("WD make INIT")

    def create_web_driver(self) -> WD:
        if self.web_driver is not None:
            return self

        frame = inspect.currentframe()

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['enableVNC'] = True
        capabilities['name'] = whoami(frame)

        chrome_options = Options()

        chrome_prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }

        chrome_options.add_experimental_option("prefs", chrome_prefs)

        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")

        # TODO Make auto-detect needless mobile emulation
        if os.environ["MOBILE_EMULATION"] != "False":
            chrome_options.add_experimental_option(
                "mobileEmulation",
                {
                    "deviceMetrics": {
                        "width": 360,
                        "height": 0,  # 0-значение высоты экрана эмулятора привяжет её к высоте окна браузера
                        "pixelRatio": 3.0
                    },
                    "userAgent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Mobile Safari/537.36"
                })

        command_executor = os.environ["GGR_PLAYBACK_HOST"]
        if not command_executor:
            raise Exception("Do not set GGR_PLAYBACK_HOST in config-file! Set it, please!")

        self.web_driver = webdriver.Remote(
            command_executor=command_executor,
            desired_capabilities=capabilities,
            options=chrome_options
        )

        if self.web_driver is None:
            raise Exception("Could not create WebDriver Remote instance! Test could not started")

        return self

    def quit(self):
        self.web_driver.quit()

    def open_relative_url(self, relative_url: str):
        self.web_driver.get(env.get_base_url() + relative_url)


def whoami(frame):
    return inspect.getframeinfo(frame).function
