from __future__ import annotations
from typing import Optional


class WebDavScreenshotStorageData:
    def __init__(self):
        self.__screenshots_dir_name: Optional[str] = None
        self.__screenshot_url_without_prefix: Optional[str] = None
        self.__full_screenshots_dir_url: Optional[str] = None
        self.__full_screenshot_url: Optional[str] = None

    @property
    def screenshots_dir_name(self) -> str:
        return self.__screenshots_dir_name

    @property
    def screenshot_url_without_prefix(self) -> Optional[str]:
        return self.__screenshot_url_without_prefix

    @property
    def full_screenshots_dir_url(self) -> Optional[str]:
        return self.__full_screenshots_dir_url

    @property
    def full_screenshot_url(self) -> Optional[str]:
        return self.__full_screenshot_url

    def set_screenshots_dir_name(self, dir_name: str) -> WebDavScreenshotStorageData:
        self.__screenshots_dir_name = dir_name
        return self

    def set_screenshot_url_without_prefix(self, url: str) -> WebDavScreenshotStorageData:
        self.__screenshot_url_without_prefix = url
        return self

    def set_full_screenshots_dir_url(self, dir_url: str) -> WebDavScreenshotStorageData:
        self.__full_screenshots_dir_url = dir_url
        return self

    def set_full_screenshot_url(self, full_url: str) -> WebDavScreenshotStorageData:
        self.__full_screenshot_url = full_url
        return self
