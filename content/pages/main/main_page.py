from __future__ import annotations

from acceptance_core_py.core.actions import waiting_actions
from content.blocks.desktop.header_menu.header_menu_block import HeaderMenuBlock
from testing_projects_common.pages.base_page import BasePage


class MainPage(BasePage):
    __header_menu_block = None

    @property
    def header_menu_block(self) -> HeaderMenuBlock:
        if self.__header_menu_block is None:
            self.__header_menu_block = HeaderMenuBlock()
        return self.__header_menu_block

    def wait_for_ready(self):
        waiting_actions.wait_for_load()
        waiting_actions.wait_for_element_visible(
            self.header_menu_block.me,
            "Could not waiting for visibility Header menu block",
        )

    # Page interactive methods...

    def click_men_section_and_open_main_page(self) -> MainPage:
        self.header_menu_block.click_open_men_section()
        self.wait_for_ready()
        return self
