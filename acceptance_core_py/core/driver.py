from __future__ import annotations

import os

import logging
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from acceptance_core_py.core.exception.at_exception import ATException
from acceptance_core_py.helpers import env

instance: WebDriver


def initialize() -> WebDriver:
    global instance

    command_executor_url = os.environ["GGR_PLAYBACK_HOST"]
    if not command_executor_url:
        raise ATException("Do not set GGR_PLAYBACK_HOST in config-file! Set it, please!")

    logging.info("Creating WebDriver Remote instance by " + command_executor_url)
    test_name_for_show = env.get_test_file_name() + "::" + env.get_test_name()

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['enableVNC'] = True
    capabilities['name'] = test_name_for_show

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

    if env.is_enable_mobile_emulation_mode():
        logging.info("Enabling mobile emulation mode")
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

    try:
        instance = webdriver.Remote(
            command_executor=command_executor_url,
            desired_capabilities=capabilities,
            options=chrome_options
        )
    except Exception:
        raise ATException("Could not create WebDriver Remote instance by " + command_executor_url + ". Test cannot start")

    return instance


def close_driver():
    global instance
    logging.info("Quit WebDriver. Bye-bye")
    instance.quit()
