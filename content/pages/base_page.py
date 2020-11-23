from __future__ import annotations
from abc import ABC, abstractmethod

from selenium.webdriver.remote.webelement import WebElement

from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.selector import Selector
from content.url_builders.base_url_builder import BaseUrlBuilder


class BasePage(ABC):

    @abstractmethod
    def wait_for_ready(self):
        pass

    @property
    def body_selector(self) -> Selector:
        return Selector('html').child_by_tag('body')

    @property
    def body_element(self) -> WebElement:
        return self.body_selector.web_element

    def open_me(self, page_url_builder: BaseUrlBuilder) -> BasePage:
        open_url = page_url_builder.get_url_to_open()
        driver_actions.open_direct_url(open_url)
        self.wait_for_ready()
        return self
