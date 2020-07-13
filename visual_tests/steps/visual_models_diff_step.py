import logging
from typing import Optional

import pytest
from diffimg import diff
from selenium.webdriver.remote.webelement import WebElement

from acceptance_core_py.core.actions import screenshot_actions_keys
from acceptance_core_py.core.actions.screenshot_actions import ScreenshotActions
from acceptance_core_py.core.visual_tests.visual_models_actions import VisualModelsActions
from acceptance_core_py.helpers import env
from acceptance_core_py.helpers.clients.webdav_client import WebDavClient


def perform_reference_and_candidate_element_diff(web_element: WebElement) -> Optional[float]:
    visual_models_instance = VisualModelsActions.get_instance()
    screenshot_actions_instance = ScreenshotActions.get_instance()

    # Обработка Reference mode. Только захватывается эталон и передаем тесту None, чтобы тест завершился успешно
    if env.is_reference_mode():
        visual_models_instance.capture_reference_element_visual_model(web_element)
        logging.warning("Test in Reference capturing mode. It's all done")
        return None

    reference_local_model_data = screenshot_actions_instance.create_screenshot_local_storage_data(
        screenshot_actions_keys.reference_model_local_postfix)

    # Загружаем reference из WebDav в локаль в папку артифактов теста
    if not visual_models_instance.download_reference_visual_model(reference_local_model_data):
        pytest.fail("Could not download branch or master reference model. "
                    "It's bad, please create reference visual model for test!")

    # Загружаем reference в WebDav в папку результатов работы теста
    WebDavClient().publish_screenshot(reference_local_model_data)

    # Захватываем модель-кандидата
    candidate_model_local_path = visual_models_instance.capture_candidate_element_visual_model(web_element)

    # Обрабатываем Diff скриншот, создаем local storage data, сохраняем по ней diff-скриншот
    diff_image_local_storage_data = screenshot_actions_instance.create_screenshot_local_storage_data('diff')
    diff_image_local_path = diff_image_local_storage_data.full_local_screenshot_path

    diff_percent = diff(str(reference_local_model_data.full_local_screenshot_path.absolute()),
                        str(candidate_model_local_path.absolute()),
                        diff_img_file=str(diff_image_local_path.absolute()),
                        ignore_alpha=True)

    # Diff-скриншот тоже загружаем в WebDav для легкого дебага теста
    WebDavClient().publish_screenshot(diff_image_local_storage_data)

    rounded_diff_percent = round(diff_percent, 2)
    logging.warning(f"Reference model VS Candidate model diff is: {rounded_diff_percent=}")
    return rounded_diff_percent
