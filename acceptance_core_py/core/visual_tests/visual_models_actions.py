import logging
from pathlib import Path
from typing import Optional

from PIL import Image
from selenium.webdriver.remote.webelement import WebElement

from acceptance_core_py.core.actions.screenshot_actions import ScreenshotActions
from acceptance_core_py.core.actions import screenshot_actions_keys
from acceptance_core_py.core.actions.screenshot_local_storage_data import ScreenshotLocalStorageData
from acceptance_core_py.helpers import env
from acceptance_core_py.helpers.clients.webdav_client import WebDavClient


class VisualModelsActions:
    """Attention: Singleton object, use by VisualModelsActions.get_instance()"""
    __instance = None

    __references_dir_name_in_webdav = 'acceptance-visual-models'

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = VisualModelsActions()
        return cls.__instance

    def get_reference_publishing_cloud_url(self, force_gitlab_master_branch: bool = False) -> str:
        """Generate and get future uploaded screenshot url in WebDav"""
        screenshot_local_storage_data = self.__create_screenshot_local_storage_data()

        # Add Gitlab branch name to screenshot path data
        if force_gitlab_master_branch:
            gitlab_branch_name = 'master'
        else:
            gitlab_branch_name = env.get_git_branch_name()
        screenshot_local_storage_data.set_gitlab_branch_name(gitlab_branch_name)

        webdav_client = WebDavClient(self.__references_dir_name_in_webdav)
        return webdav_client.create_webdav_screenshot_storage_data(screenshot_local_storage_data).full_screenshot_url

    def capture_reference_element_visual_model(self, element: WebElement) -> bool:
        screenshot_local_storage_data = self.__create_screenshot_local_storage_data()

        # Add Gitlab branch name to screenshot path data
        gitlab_branch_name = env.get_git_branch_name()
        screenshot_local_storage_data.set_gitlab_branch_name(gitlab_branch_name)

        is_successfully_saved = ScreenshotActions.get_instance().create_and_save_screenshot_in_local(
            screenshot_local_storage_data)

        if is_successfully_saved:
            self.__crop_by_element(screenshot_local_storage_data.full_local_screenshot_path, element)

            webdav_client = WebDavClient(self.__references_dir_name_in_webdav)
            webdav_client.publish_screenshot(screenshot_local_storage_data)
            return True
        return False

    def capture_candidate_element_visual_model(self, element: WebElement) -> Optional[Path]:
        """Return local screenshot Path"""
        screenshot_local_storage_data = ScreenshotActions.get_instance().create_screenshot_local_storage_data(
            'candidate_model')
        is_successfully_saved = ScreenshotActions.get_instance().create_and_save_screenshot_in_local(
            screenshot_local_storage_data)

        if is_successfully_saved:
            screenshot_local_path = screenshot_local_storage_data.full_local_screenshot_path
            self.__crop_by_element(screenshot_local_path, element)
            WebDavClient().publish_screenshot(screenshot_local_storage_data)
            return screenshot_local_path
        return None

    def download_reference_visual_model(self,
                                        reference_local_model_data:
                                        Optional[ScreenshotLocalStorageData] = None) -> bool:
        if not reference_local_model_data:
            reference_local_model_data = ScreenshotActions.get_instance().create_screenshot_local_storage_data(
                screenshot_actions_keys.reference_model_local_postfix)
        reference_model_cloud_url = self.get_reference_publishing_cloud_url()

        # If not exists reference visual models for custom branch, try downloading master reference model
        if not WebDavClient().download_file(reference_model_cloud_url, reference_local_model_data):
            logging.info(f"Could not download reference visual model from {reference_model_cloud_url=}. "
                         "Let's try download master reference model")
            reference_model_cloud_master_url = self.get_reference_publishing_cloud_url(force_gitlab_master_branch=True)

            if not WebDavClient().download_file(reference_model_cloud_master_url, reference_local_model_data):
                logging.warning(f"Could not download master reference visual model from {reference_model_cloud_url=}")
                return False
        return True

    def __crop_by_element(self, screenshot_local_path: Path, element: WebElement):
        """Crop full page screenshot by target element. Element coordinates calculates automatically"""
        location = element.location
        size = element.size
        x = location['x']
        y = location['y']
        width = location['x'] + size['width']
        height = location['y'] + size['height']

        im = Image.open(screenshot_local_path)
        im = im.crop((int(x), int(y), int(width), int(height)))
        im.save(screenshot_local_path)

    def __create_screenshot_local_storage_data(self) -> ScreenshotLocalStorageData:
        """Create local storage data for future screenshot"""
        screenshot_local_storage_data = ScreenshotLocalStorageData()

        test_file_name = env.get_test_file_name().replace("/", "_").replace(".", "_")
        screenshots_path = Path(f"output/models/{test_file_name}/")
        screenshot_file_name = f"{test_file_name}.png"
        screenshot_path_with_file_name = screenshots_path / screenshot_file_name

        screenshot_local_storage_data.set_screenshots_dir_name(test_file_name)
        screenshot_local_storage_data.set_local_dir_path(screenshots_path)
        screenshot_local_storage_data.set_screenshot_file_name(screenshot_file_name)
        screenshot_local_storage_data.set_full_local_screenshot_path(screenshot_path_with_file_name)

        return screenshot_local_storage_data
