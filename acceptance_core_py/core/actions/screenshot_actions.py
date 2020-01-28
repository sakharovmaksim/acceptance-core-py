import logging
import os
import pathlib

from acceptance_core_py.core import driver
from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.helpers import env
from acceptance_core_py.helpers.utils import date_utils


class ScreenshotActions:
    """Attention: Singleton object, use by ScreenshotActions.get_instance()"""
    __instance = None
    # Screenshots from one test should be saved in one folder
    screenshots_dir_name_postfix = ""

    def __init__(self):
        if not ScreenshotActions.__instance:
            self.screenshots_dir_name_postfix = date_utils.generate_date(format_date="%Y-%m-%d-%H-%M-%S")

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = ScreenshotActions()
        return cls.__instance

    def capture_screenshot(self, screenshot_name_postfix: str = None) -> str:
        append_to_screenshot_file_name = ""
        if screenshot_name_postfix:
            append_to_screenshot_file_name = "_" + screenshot_name_postfix

        path = os.path.abspath(os.getcwd()).__str__()
        test_file_name = env.get_test_file_name().replace("/", "_").replace(".", "_")

        # Example: test_screenshots-2020-01-22-20-03-53
        screenshot_dir_name = env.get_test_name() + "-" + self.screenshots_dir_name_postfix
        # Example: /zoon/acceptance-selenium-tests-my/output/screenshots/test_screenshots-2020-01-22-20-03-53/
        screenshot_path_without_file = f"{path}/output/screenshots/{screenshot_dir_name}"

        date_for_test = "_" + date_utils.generate_date(format_date="%H_%M_%S_%f")
        # Example: test_correctly_opening_pages_py_test_screenshots_20_03_54_889506.png
        screenshot_file_name = f"{test_file_name}_{env.get_test_name()}{append_to_screenshot_file_name}{date_for_test}.png"

        # Example: /zoon/acceptance-selenium-tests-my/output/screenshots/test_screenshots-2020-01-22-20-03-53/test_correctly_opening_pages_py_test_screenshots_20_03_54_889506.png
        screenshot_path_with_file = f"{screenshot_path_without_file}/{screenshot_file_name}"
        pathlib.Path(screenshot_path_without_file).mkdir(parents=True, exist_ok=True)

        # Make full page screenshot (hacking)
        window_width = int(driver_actions.execute_js('return window.innerWidth'))
        page_height = int(driver_actions.execute_js('return document.body.scrollHeight'))
        # Add a few pixels so that the picture is not cropped from the bottom
        driver_actions.set_window_size(window_width, page_height + 250)

        logging.info(f"Saving screenshot in path: '{screenshot_path_with_file}'")
        status = driver.instance.save_screenshot(screenshot_path_with_file)
        if status:
            logging.info(f"Successfully saved screenshot in local: '{screenshot_path_with_file}'")
            # You can add uploading screenshot to Cloud storage, like S3 or WebDav
            return screenshot_path_with_file
        logging.error(f"Failed with savings screenshot in '{screenshot_path_with_file}'")
        return ""
