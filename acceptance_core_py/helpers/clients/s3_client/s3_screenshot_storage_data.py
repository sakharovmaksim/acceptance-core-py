from __future__ import annotations


class S3ScreenshotStorageData:
    def __init__(self):
        self.__screenshots_dir_name: str | None = None
        self.__screenshot_url_without_prefix: str | None = None
        self.__full_screenshots_dir_url: str | None = None
        self.__full_screenshot_url: str | None = None

    @property
    def screenshots_dir_name(self) -> str:
        return self.__screenshots_dir_name

    @property
    def screenshot_url_without_prefix(self) -> str | None:
        return self.__screenshot_url_without_prefix

    @property
    def full_screenshots_dir_url(self) -> str | None:
        return self.__full_screenshots_dir_url

    @property
    def full_screenshot_url(self) -> str | None:
        return self.__full_screenshot_url

    def set_screenshots_dir_name(self, dir_name: str) -> S3ScreenshotStorageData:
        self.__screenshots_dir_name = dir_name
        return self

    def set_screenshot_url_without_prefix(self, url: str) -> S3ScreenshotStorageData:
        self.__screenshot_url_without_prefix = url
        return self

    def set_full_screenshots_dir_url(self, dir_url: str) -> S3ScreenshotStorageData:
        self.__full_screenshots_dir_url = dir_url
        return self

    def set_full_screenshot_url(self, full_url: str) -> S3ScreenshotStorageData:
        self.__full_screenshot_url = full_url
        return self
