import logging
from typing import Optional

import allure
import pytest
from selenium.webdriver.remote.webelement import WebElement

from acceptance_core_py.core.actions import screenshot_actions_keys
from acceptance_core_py.core.actions.screenshot_actions import ScreenshotActions
from acceptance_core_py.core.visual_tests.images_diff_helper import (
    get_images_diff_percent_and_save_diff_img,
)
from acceptance_core_py.core.visual_tests.visual_models_actions import (
    VisualModelsActions,
)
from acceptance_core_py.helpers import env
from acceptance_core_py.helpers.clients.s3_client.s3_client import S3Client
from acceptance_core_py.helpers.clients.sentry_client import SentryClient


def perform_reference_and_candidate_element_diff(
    web_element: WebElement,
) -> Optional[float]:
    visual_models_instance = VisualModelsActions.get_instance()
    screenshot_actions_instance = ScreenshotActions.get_instance()

    # Обработка Reference mode. Только захватывается эталон и передаем тесту None, чтобы тест завершился успешно
    if env.is_reference_mode():
        visual_models_instance.capture_reference_element_visual_model(web_element)
        # Это реализация девелопер-режима, нужен чтобы при разработке не дергать постоянно reference и testing-режимы
        if not env.is_testing_mode():
            logging.warning("Test in Reference capturing mode. It's all done!")
            return None

    reference_local_model_data = (
        screenshot_actions_instance.create_screenshot_local_storage_data(
            screenshot_actions_keys.reference_model_local_postfix
        )
    )

    # Загружаем reference из s3 в локаль в папку артефактов теста
    if not visual_models_instance.download_reference_visual_model(
        reference_local_model_data
    ):
        pytest.fail(
            "Could not download branch or master reference model. "
            "It's bad, please create reference visual model for test!"
        )

    # Загружаем reference в S3 в папку результатов работы теста
    S3Client().publish_screenshot(reference_local_model_data)

    # Захватываем модель-кандидата
    candidate_model_local_path = (
        visual_models_instance.capture_candidate_element_visual_model(web_element)
    )

    # Обрабатываем Diff скриншот, создаем local storage data, сохраняем по ней diff-скриншот
    diff_image_local_storage_data = (
        screenshot_actions_instance.create_screenshot_local_storage_data("diff")
    )
    diff_image_local_path = diff_image_local_storage_data.full_local_screenshot_path

    diff_percent = get_images_diff_percent_and_save_diff_img(
        reference_local_model_data.full_local_screenshot_path,
        candidate_model_local_path,
        diff_image_local_path,
    )
    # Прикрепляем Diff в Allure
    allure.attach.file(diff_image_local_path, "Различия", allure.attachment_type.PNG)

    # Diff-скриншот тоже загружаем в S3 для легкого дебага теста
    s3_client = S3Client()
    s3_client.publish_screenshot(diff_image_local_storage_data)

    # Сеттим в SentryClient инстанс ссылку на папку со скриншотами для отображения в событии Sentry
    created_s3_screenshot_storage_data = s3_client.created_s3_screenshot_storage_data
    if (
        created_s3_screenshot_storage_data
        and created_s3_screenshot_storage_data.full_screenshots_dir_url
    ):
        s3_screenshots_dir_url = (
            created_s3_screenshot_storage_data.full_screenshots_dir_url
        )
        logging.debug(f"Setting in SentryClient instance {s3_screenshots_dir_url=}")
        SentryClient.get_instance().set_screenshot_url(s3_screenshots_dir_url)

    logging.warning(f"Reference model VS Candidate model diff is: {diff_percent=}")
    return diff_percent
