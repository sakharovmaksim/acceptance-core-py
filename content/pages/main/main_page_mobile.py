from __future__ import annotations

from acceptance_core_py.core.actions import waiting_actions
from content.blocks.mobile.header_cart_block import HeaderCartBlock
from content.pages.base_page import BasePage


class MainPageMobile(BasePage):
    __header_cart_block = None

    @property
    def header_cart_block(self) -> HeaderCartBlock:
        if self.__header_cart_block is None:
            self.__header_cart_block = HeaderCartBlock()
        return self.__header_cart_block

    def wait_for_ready(self):
        waiting_actions.wait_for_load()
        waiting_actions.wait_for_element_visible(self.header_cart_block.me,
                                                 'Could not waiting for Header Cart block visible', 10)
