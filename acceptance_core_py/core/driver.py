from __future__ import annotations

import logging
import os

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from acceptance_core_py.core.exception.at_exception import ATException
from acceptance_core_py.core.selenoid_playback import SelenoidPlayback
from acceptance_core_py.helpers import env

instance: WebDriver

mobile_mode: bool = False


def initialize() -> WebDriver:
    global instance

    command_executor_url = SelenoidPlayback().command_executor_url

    logging.info("Creating WebDriver Remote instance by " + command_executor_url)
    test_name_for_show = env.get_test_file_name() + "::" + env.get_test_name()

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities["enableVNC"] = True
    capabilities["name"] = test_name_for_show

    browser_version = str(os.environ["BROWSER_VERSION"])
    if browser_version and browser_version != "DEFAULT":
        logging.info(
            f"Requested browser version '{browser_version}'. Setting this version for browser"
        )
        capabilities["version"] = browser_version

    chrome_options = Options()

    chrome_prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    }

    chrome_options.add_experimental_option("prefs", chrome_prefs)
    # Tap do not work without it
    # https://stackoverflow.com/questions/56111529/cannot-call-non-w3c-standard-command-while-in-w3c-mode-seleniumwebdrivererr
    chrome_options.add_experimental_option("w3c", False)

    if env.is_headless_mode():
        logging.info("Enabling 'headless mode' for browser instance")
        chrome_options.headless = True
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--ignore-certificate-errors")

    if mobile_mode:
        logging.info("Enabling mobile emulation mode for browser instance")
        chrome_options.add_experimental_option(
            "mobileEmulation",
            {
                "deviceMetrics": {
                    "width": 360,
                    "height": 0,  # 0-значение высоты экрана эмулятора привяжет её к высоте окна браузера
                    "pixelRatio": 3.0,
                },
                "userAgent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, "
                "like Gecko) Chrome/%s Mobile Safari/537.36 ",
            },
        )

    try:
        instance = webdriver.Remote(
            command_executor=command_executor_url,
            desired_capabilities=capabilities,
            options=chrome_options,
        )
    except Exception:
        raise ATException(
            f"Could not create WebDriver Remote instance by {command_executor_url}. Test cannot start"
        )

    return instance


def close_driver():
    global instance
    logging.info("Quit WebDriver instance. Bye-bye!")
    instance.quit()
