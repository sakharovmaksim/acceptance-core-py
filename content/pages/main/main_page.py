from __future__ import annotations

from acceptance_core_py.core.actions import waiting_actions
from content.blocks.header_menu.header_menu_block import HeaderMenuBlock
from content.blocks.title.title_block import TitleBlock
from content.pages.base_page import BasePage


class MainPage(BasePage):
    title_block = None
    header_menu_block = None

    def get_title_block(self) -> TitleBlock:
        if self.title_block is None:
            self.title_block = TitleBlock()
        return self.title_block

    def get_header_menu_block(self) -> HeaderMenuBlock:
        if self.header_menu_block is None:
            self.header_menu_block = HeaderMenuBlock()
        return self.header_menu_block

    def wait_for_ready(self):
        waiting_actions.wait_for_load()
        waiting_actions.wait_for_element_visible(
            self.get_header_menu_block().me.__str__(), "Could not waiting for visibility Header menu block")

    # Page interactive methods...

    def click_men_section_and_open_main_page(self) -> MainPage:
        self.get_header_menu_block().click_open_men_section()
        self.wait_for_ready()
        return self
