from __future__ import annotations

import logging
import pathlib
from typing import Optional

import requests
from webdav3.client import Client

from acceptance_core_py.core.actions.screenshot_local_storage_data import (
    ScreenshotLocalStorageData,
)
from acceptance_core_py.core.exception.at_exception import ATException
from acceptance_core_py.helpers.clients import webdav_keys
from acceptance_core_py.helpers.clients.webdav_screenshot_storage_data import (
    WebDavScreenshotStorageData,
)


class WebDavClient:
    __created_webdav_screenshot_storage_data: None | (
        WebDavScreenshotStorageData
    ) = None

    __options = {
        "webdav_hostname": webdav_keys.webdav_hostname,
        "webdav_login": webdav_keys.webdav_login,
        "webdav_password": webdav_keys.webdav_password,
    }

    def __init__(self, screenshots_base_dir: str = "acceptance-screenshots-py"):
        logging.debug("Creating WebDav client")
        self.__screenshots_base_dir = screenshots_base_dir
        self.__client = Client(self.__options)
        if not self.__client.check(self.__screenshots_base_dir):
            self.__client.mkdir(self.__screenshots_base_dir)

    @property
    def created_webdav_screenshot_storage_data(
        self,
    ) -> WebDavScreenshotStorageData | None:
        return self.__created_webdav_screenshot_storage_data

    def create_webdav_screenshot_storage_data(
        self, screenshot_local_storage_data: ScreenshotLocalStorageData
    ) -> WebDavScreenshotStorageData:
        webdav_screenshot_storage_data = WebDavScreenshotStorageData()
        gitlab_branch_name = None

        if screenshot_local_storage_data.gitlab_branch_name:
            gitlab_branch_name = screenshot_local_storage_data.gitlab_branch_name

        remote_dir_name = screenshot_local_storage_data.screenshots_dir_name
        screenshot_file_name = screenshot_local_storage_data.screenshot_file_name

        if gitlab_branch_name:
            webdav_dir_for_upload = (
                self.__screenshots_base_dir
                + "/"
                + gitlab_branch_name
                + "/"
                + remote_dir_name
            )
        else:
            webdav_dir_for_upload = self.__screenshots_base_dir + "/" + remote_dir_name

        login = webdav_keys.webdav_login
        password = webdav_keys.webdav_password
        hostname = webdav_keys.webdav_hostname.replace("http://", "")
        url_prefix = f"http://{login}:{password}@{hostname}" + "/"

        webdav_screenshot_storage_data.set_full_screenshots_dir_url(
            url_prefix + webdav_dir_for_upload + "/"
        )

        screenshot_url_without_prefix = (
            webdav_dir_for_upload + "/" + screenshot_file_name
        )
        full_screenshot_url = url_prefix + screenshot_url_without_prefix

        webdav_screenshot_storage_data.set_screenshots_dir_name(webdav_dir_for_upload)
        webdav_screenshot_storage_data.set_screenshot_url_without_prefix(
            screenshot_url_without_prefix
        )
        webdav_screenshot_storage_data.set_full_screenshot_url(full_screenshot_url)

        self.__created_webdav_screenshot_storage_data = webdav_screenshot_storage_data
        return webdav_screenshot_storage_data

    def publish_screenshot(
        self, screenshot_local_storage_data: ScreenshotLocalStorageData
    ) -> str | None:
        logging.info("Publishing local screenshot to WebDav cloud storage...")

        webdav_screenshot_storage_data = self.create_webdav_screenshot_storage_data(
            screenshot_local_storage_data
        )
        webdav_dir_for_upload: str = webdav_screenshot_storage_data.screenshots_dir_name
        webdav_file_uploaded_url: str = (
            webdav_screenshot_storage_data.screenshot_url_without_prefix
        )
        full_screenshot_url: str = webdav_screenshot_storage_data.full_screenshot_url

        screenshot_local_path = screenshot_local_storage_data.full_local_screenshot_path

        if not self.__client.check(webdav_dir_for_upload):
            logging.debug(
                f"Creating WebDav-dir for screenshot: '{webdav_dir_for_upload=}'"
            )
            dir_list = webdav_dir_for_upload.split("/")
            if len(dir_list) == 2:
                self.__client.mkdir(webdav_dir_for_upload)
            elif len(dir_list) == 3:
                self.__client.mkdir(dir_list[0] + "/" + dir_list[1])
                self.__client.mkdir(dir_list[0] + "/" + dir_list[1] + "/" + dir_list[2])
            else:
                raise ATException(
                    f"{dir_list=} not supported for creating dirs in WebDav"
                )

        try:
            self.__client.upload_sync(webdav_file_uploaded_url, screenshot_local_path)
        except Exception:
            logging.warning(
                f"Could not upload screenshot from '{screenshot_local_path=}' "
                f"to WebDav {webdav_file_uploaded_url=}"
            )
            return None

        logging.warning(f"--- Uploaded SCREENSHOT URL is: '{full_screenshot_url}' ---")
        return full_screenshot_url

    def download_file(
        self, from_url: str, screenshot_local_storage_data: ScreenshotLocalStorageData
    ) -> bool:
        local_dir_path = screenshot_local_storage_data.local_dir_path
        full_local_file_path = screenshot_local_storage_data.full_local_screenshot_path
        logging.info(
            f"Downloading file from WebDav. From '{from_url=}', saving to '{full_local_file_path=}'"
        )

        pathlib.Path(local_dir_path).mkdir(parents=True, exist_ok=True)
        img_data = requests.get(
            from_url, auth=(webdav_keys.webdav_login, webdav_keys.webdav_password)
        ).content

        min_file_size_bytes = 300
        if img_data.__sizeof__() < min_file_size_bytes:
            logging.info(
                f"File by {from_url=} is less than {min_file_size_bytes=}. "
                "Do not save this file in local, maybe file is empty"
            )
            return False

        with full_local_file_path.open("wb") as file:
            file.write(img_data)
        return True
