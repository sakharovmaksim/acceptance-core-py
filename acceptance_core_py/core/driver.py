from __future__ import annotations

import os

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

instance = None


def initialize():
    global instance
    print("\nCreating WebDriver instance")

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['enableVNC'] = True
    capabilities['name'] = "ui test powered by Python"

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

    instance = webdriver.Remote(
        command_executor=command_executor,
        desired_capabilities=capabilities,
        options=chrome_options
    )
    instance.implicitly_wait(5)

    if instance is None:
        raise Exception("Could not create WebDriver Remote instance! Test could not started")

    return instance


def close_driver():
    global instance
    print("Quit WebDriver. Bye-bye")
    instance.quit()
