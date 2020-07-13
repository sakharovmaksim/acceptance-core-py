from __future__ import annotations

from pathlib import Path
from typing import Optional


class ScreenshotLocalStorageData:
    def __init__(self):
        self.__screenshots_dir_name: Optional[str] = None
        self.__local_dir_path: Optional[Path] = None
        self.__screenshot_file_name: Optional[str] = None
        self.__full_local_screenshot_path: Optional[Path] = None
        self.__gitlab_branch_name: Optional[str] = None

    @property
    def screenshots_dir_name(self) -> Optional[str]:
        return self.__screenshots_dir_name

    @property
    def local_dir_path(self) -> Optional[Path]:
        return self.__local_dir_path

    @property
    def screenshot_file_name(self) -> Optional[str]:
        return self.__screenshot_file_name

    @property
    def full_local_screenshot_path(self) -> Optional[Path]:
        return self.__full_local_screenshot_path

    @property
    def gitlab_branch_name(self) -> Optional[str]:
        return self.__gitlab_branch_name

    def set_screenshots_dir_name(self, dir_name: str) -> ScreenshotLocalStorageData:
        self.__screenshots_dir_name = dir_name
        return self

    def set_local_dir_path(self, dir_path: Path) -> ScreenshotLocalStorageData:
        self.__local_dir_path = dir_path
        return self

    def set_screenshot_file_name(self, screenshot_file_name: str) -> ScreenshotLocalStorageData:
        self.__screenshot_file_name = screenshot_file_name
        return self

    def set_full_local_screenshot_path(self, full_screenshot_path: Path) -> ScreenshotLocalStorageData:
        self.__full_local_screenshot_path = full_screenshot_path
        return self

    def set_gitlab_branch_name(self, branch_name: str) -> ScreenshotLocalStorageData:
        self.__gitlab_branch_name = branch_name
        return self
