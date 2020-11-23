from __future__ import annotations

import logging
from abc import ABC
from typing import Optional

from selenium.webdriver.remote.webelement import WebElement

from acceptance_core_py.core.actions import driver_actions, waiting_actions
from acceptance_core_py.core.selector import Selector


class Block(ABC):
    block_class = None
    block_class_contains = None
    block_id = None
    block_tag = None
    block_attribute_name = None
    block_attribute_value = None
    custom_wait_timeout_in_sec: Optional[int] = None

    selector = Selector

    def __init__(self, selector=None):
        if selector is None:
            selector = Selector("")
        if isinstance(selector, Selector):
            self.selector = self.get_block_selector_from_context_selector(selector)
        else:
            # If selector is string or something else...
            self.selector = Selector(str(selector))

    def __str__(self):
        """Return Block's Selector instance as string"""
        return self.me.__str__()

    @property
    def me(self) -> Selector:
        return self.selector

    @property
    def web_element(self) -> WebElement:
        return driver_actions.locate_element(self.selector)

    def get_block_selector_from_context_selector(self, context_selector: Selector) -> Selector:
        if self.block_class:
            return context_selector.child_by_class(self.block_class)
        elif self.block_class_contains:
            return context_selector.child_by_class_contains(self.block_class_contains)
        elif self.block_id:
            return context_selector.child_by_id(self.block_id)
        elif self.block_tag:
            return context_selector.child_by_tag(self.block_tag)
        elif self.block_attribute_name and self.block_attribute_value:
            return context_selector.child_by_attribute(self.block_attribute_name, self.block_attribute_value)
        else:
            logging.debug(f"Block do not have your own content selector, "
                          f"return 'context_selector': '{context_selector}'")
            return context_selector

    def wait_for_ready(self) -> Block:
        waiting_actions.wait_for_element_visible(
            self.me, f"Could not waiting for visibility {self.__class__.__name__}", self.custom_wait_timeout_in_sec)
        return self
