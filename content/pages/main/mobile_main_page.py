from __future__ import annotations

from acceptance_core_py.core.actions import waiting_actions
from content.blocks.title.title_block import TitleBlock
from content.pages.base_page import BasePage


class MobileMainPage(BasePage):
    __title_block = None

    @property
    def title_block(self) -> TitleBlock:
        if self.__title_block is None:
            self.__title_block = TitleBlock()
        return self.__title_block

    def wait_for_ready(self):
        waiting_actions.wait_for_load()
        waiting_actions.wait_for_element_exists(self.title_block.me, 'Could not waiting for Title visibility', 10)
