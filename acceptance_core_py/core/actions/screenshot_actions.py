import logging
import pathlib
from pathlib import Path
from typing import Optional

from acceptance_core_py.core import driver
from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.actions.screenshot_local_storage_data import ScreenshotLocalStorageData
from acceptance_core_py.helpers import env
from acceptance_core_py.helpers.utils import date_utils
from acceptance_core_py.helpers.clients.webdav_client import WebDavClient


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
            logging.debug("Creating ScreenshotActions instance")
            cls.__instance = ScreenshotActions()
        return cls.__instance

    def capture_full_page_screenshot(self, screenshot_name_postfix: str = None) -> Optional[str]:
        """Return uploaded screenshot URL in WebDav storage"""
        screenshot_url = None

        screenshot_local_storage_data = self.create_screenshot_local_storage_data(screenshot_name_postfix)
        is_successfully_saved = self.create_and_save_screenshot_in_local(screenshot_local_storage_data)
        if is_successfully_saved:
            uploaded_screenshot_url = WebDavClient().publish_screenshot(screenshot_local_storage_data)
            screenshot_url = uploaded_screenshot_url
        return screenshot_url

    def create_and_save_screenshot_in_local(self, screenshot_local_storage_data: ScreenshotLocalStorageData) -> bool:
        """Make and save screenshot in local dir. Return origin screenshot_path_data if success"""
        dir_path_for_screenshot = screenshot_local_storage_data.local_dir_path
        screenshot_path_with_file: Path = screenshot_local_storage_data.full_local_screenshot_path

        pathlib.Path(dir_path_for_screenshot).mkdir(parents=True, exist_ok=True)

        # Make full page screenshot (hacking)
        window_width = int(driver_actions.execute_js('return window.innerWidth'))
        page_height = int(driver_actions.execute_js('return document.body.scrollHeight'))
        # Add a few pixels so that the picture is not cropped from the bottom
        driver_actions.set_window_size(window_width, page_height + 250)

        logging.info(f"Saving screenshot in path: '{screenshot_path_with_file}'")
        status = driver.instance.save_screenshot(str(screenshot_path_with_file.absolute()))
        if status:
            logging.info(f"Successfully saved screenshot in local storage: '{screenshot_path_with_file=}'")
            return True

        logging.warning(f"Failed on saving screenshot in '{screenshot_path_with_file=}'")
        return False

    def create_screenshot_local_storage_data(self, screenshot_name_postfix: str = None) -> ScreenshotLocalStorageData:
        """Return local storage data for in future saved screenshot"""
        screenshot_local_storage_data = ScreenshotLocalStorageData()

        append_to_screenshot_file_name = ""
        if screenshot_name_postfix:
            append_to_screenshot_file_name = "_" + screenshot_name_postfix

        # Example: test_screenshots-2020-01-22-20-03-53
        screenshots_dir_name = env.get_test_name() + "-" + self.screenshots_dir_name_postfix
        # Example: /zoon/acceptance-selenium-tests-my/output/screenshots/test_screenshots-2020-01-22-20-03-53/
        screenshots_dir_path = Path(f"output/screenshots/{screenshots_dir_name}/")

        test_file_name = env.get_test_file_name().replace("/", "_").replace(".", "_")
        date_for_test = "_" + date_utils.generate_date(format_date="%H_%M_%S_%f")
        # Example: test_correctly_opening_pages_py_test_screenshots_20_03_54_889506.png
        screenshot_file_name = \
            f"{test_file_name}_{env.get_test_name()}{append_to_screenshot_file_name}{date_for_test}.png"
        # Example:
        # /zoon/acceptance-selenium-tests-my/output/screenshots/test_screenshots-2020-01-22-20-03-53/test_correctly_opening_pages_py_test_screenshots_20_03_54_889506.png
        screenshot_path = screenshots_dir_path / screenshot_file_name

        screenshot_local_storage_data.set_screenshots_dir_name(screenshots_dir_name)
        screenshot_local_storage_data.set_local_dir_path(screenshots_dir_path)
        screenshot_local_storage_data.set_screenshot_file_name(screenshot_file_name)
        screenshot_local_storage_data.set_full_local_screenshot_path(screenshot_path)
        return screenshot_local_storage_data
