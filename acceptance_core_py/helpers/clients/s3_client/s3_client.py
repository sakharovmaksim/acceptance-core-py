from __future__ import annotations

import logging
import os
import pathlib
from pathlib import Path

import boto3

from acceptance_core_py.core.actions.screenshot_local_storage_data import (
    ScreenshotLocalStorageData,
)
from acceptance_core_py.helpers.clients.s3_client import s3_keys
from acceptance_core_py.helpers.clients.s3_client.s3_screenshot_storage_data import (
    S3ScreenshotStorageData,
)


class S3Client:
    __created_s3_screenshot_storage_data: S3ScreenshotStorageData | None = None

    def __init__(self, screenshots_base_dir: str = "ui-tests-screenshots"):
        logging.debug("Creating s3 client")
        self.__screenshots_base_dir = screenshots_base_dir
        self.__client = boto3.client(
            service_name="s3",
            aws_access_key_id=s3_keys.aws_access_key_id,
            aws_secret_access_key=s3_keys.aws_secret_access_key,
            region_name=s3_keys.region_name,
        )

    @property
    def created_s3_screenshot_storage_data(self) -> S3ScreenshotStorageData | None:
        return self.__created_s3_screenshot_storage_data

    def create_s3_screenshot_storage_data(
        self, screenshot_local_storage_data: ScreenshotLocalStorageData
    ) -> S3ScreenshotStorageData:

        s3_screenshot_storage_data = S3ScreenshotStorageData()

        gitlab_branch_name = ""
        if screenshot_local_storage_data.gitlab_branch_name:
            gitlab_branch_name = screenshot_local_storage_data.gitlab_branch_name

        project_name = env.get_project_name()
        remote_dir_name = screenshot_local_storage_data.screenshots_dir_name
        screenshot_file_name = screenshot_local_storage_data.screenshot_file_name

        if gitlab_branch_name:
            dir_for_upload = (
                self.__screenshots_base_dir
                + "/"
                + project_name
                + "/"
                + gitlab_branch_name
                + "/"
                + remote_dir_name
            )
        else:
            dir_for_upload = (
                self.__screenshots_base_dir + "/" + project_name + "/" + remote_dir_name
            )

        hostname = s3_keys.hostname
        url_prefix = f"https://{hostname}" + "/"

        s3_screenshot_storage_data.set_full_screenshots_dir_url(
            url_prefix + dir_for_upload + "/"
        )

        screenshot_url_without_prefix = dir_for_upload + "/" + screenshot_file_name
        full_screenshot_url = url_prefix + screenshot_url_without_prefix

        s3_screenshot_storage_data.set_screenshots_dir_name(dir_for_upload)
        s3_screenshot_storage_data.set_screenshot_url_without_prefix(
            screenshot_url_without_prefix
        )
        s3_screenshot_storage_data.set_full_screenshot_url(full_screenshot_url)

        self.__created_s3_screenshot_storage_data = s3_screenshot_storage_data
        return s3_screenshot_storage_data

    def publish_screenshot(
        self, screenshot_local_storage_data: ScreenshotLocalStorageData
    ) -> str | None:
        logging.info("Publishing local screenshot to S3 cloud storage...")

        s3_screenshot_storage_data = self.create_s3_screenshot_storage_data(
            screenshot_local_storage_data
        )
        s3_file_uploaded_url: str = (
            s3_screenshot_storage_data.screenshot_url_without_prefix
        )
        full_screenshot_url: str = s3_screenshot_storage_data.full_screenshot_url
        s3_bucket_name = s3_keys.bucket_name

        screenshot_local_path_str = str(
            screenshot_local_storage_data.full_local_screenshot_path
        )

        try:
            self.__client.upload_file(
                screenshot_local_path_str,
                s3_bucket_name,
                s3_file_uploaded_url,
                ExtraArgs={"ContentType": "image/png"},
            )
        except Exception:
            logging.warning(
                f"Could not upload screenshot from '{screenshot_local_path_str=}' "
                f"to S3 {s3_file_uploaded_url=}"
            )
            return None

        logging.info(f"--- Uploaded SCREENSHOT URL is: '{full_screenshot_url}' ---")
        return full_screenshot_url

    def download_file(
        self, from_url: str, screenshot_local_storage_data: ScreenshotLocalStorageData
    ) -> bool:
        target_local_dir_path = screenshot_local_storage_data.local_dir_path
        full_local_file_path: Path = (
            screenshot_local_storage_data.full_local_screenshot_path
        )
        logging.info(
            f"Downloading file from S3. From '{from_url=}', saving to '{full_local_file_path=}'"
        )
        s3_bucket_name = s3_keys.bucket_name

        pathlib.Path(target_local_dir_path).mkdir(parents=True, exist_ok=True)
        try:
            self.__client.download_file(
                s3_bucket_name, from_url, full_local_file_path.__str__()
            )
        except Exception:
            logging.warning(
                f"Could not download screenshot from '{from_url=}' "
                f"to  {full_local_file_path=}"
            )
            return False

        min_file_size_bytes = 300
        if os.path.getsize(full_local_file_path) < min_file_size_bytes:
            logging.info(
                f"File by {from_url=} is less than {min_file_size_bytes=}, maybe file is empty"
            )
            return False
        return True
